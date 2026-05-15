"""OpenRouter SDK client, single-model call, fallback chain, validation retry and JSONL logging (M3/T26-T30)."""

import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, APITimeoutError, OpenAI, RateLimitError
from openai.types.chat import ChatCompletion

from app.validators import validator_format, validator_utf8_encoding

load_dotenv()

_BASE_URL = "https://openrouter.ai/api/v1"
_DEFAULT_HEADERS = {
    "HTTP-Referer": "https://github.com/MrChuck118/live-draft-companion",
    "X-Title": "Live Draft Companion",
}
_LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"


def get_client() -> OpenAI:
    """Return an OpenAI SDK client pointed at OpenRouter, reading the API key from env."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set in environment or .env file")
    return OpenAI(
        base_url=_BASE_URL,
        api_key=api_key,
        default_headers=_DEFAULT_HEADERS,
    )


def ping_primary_model() -> str:
    """Smoke test: send 'Dimmi solo OK' to the primary model and return its content."""
    model = os.environ.get("LLM_MODEL_PRIMARY")
    if not model:
        raise RuntimeError("LLM_MODEL_PRIMARY not set in environment or .env file")
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Dimmi solo OK"}],
    )
    return response.choices[0].message.content


def call_model(
    model_id: str,
    system: str,
    user: str,
    timeout: int = 30,
) -> ChatCompletion:
    """Single-model call with spec §9.4 parameters (temperature, max_tokens, json_object)."""
    client = get_client()
    return client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
        max_tokens=1000,
        response_format={"type": "json_object"},
        timeout=timeout,
    )


def _sleep(seconds: float) -> None:
    """Sleep wrapper, monkeypatched in tests for fast-forward."""
    time.sleep(seconds)


def _chain_from_env() -> list[str]:
    """Read the model chain from env, filtering missing fallbacks."""
    primary = os.environ.get("LLM_MODEL_PRIMARY")
    if not primary:
        raise RuntimeError("LLM_MODEL_PRIMARY not set in environment or .env file")
    chain = [primary]
    for key in ("LLM_MODEL_FALLBACK_1", "LLM_MODEL_FALLBACK_2", "LLM_MODEL_FALLBACK_3"):
        value = os.environ.get(key)
        if value:
            chain.append(value)
    return chain


def _prompt_hash(system: str, user: str) -> str:
    """Return a short stable hash of the combined prompt (no prompt content is logged)."""
    return hashlib.sha256((system + user).encode("utf-8")).hexdigest()[:16]


def _ai_call_record(
    model_id: str,
    prompt_hash: str,
    latency_ms: int,
    usage: dict | None,
    json_ok: bool,
    validation_results: dict,
    retry_count: int,
    outcome: str,
) -> dict:
    """Build one AI-call log record. `cost` is null: OpenRouter cost needs the /generation endpoint."""
    return {
        "timestamp": datetime.now().isoformat(),
        "model_used": model_id,
        "prompt_hash": prompt_hash,
        "latency_ms": latency_ms,
        "usage": usage,
        "cost": None,
        "json_ok": json_ok,
        "validation_results": validation_results,
        "retry_count": retry_count,
        "outcome": outcome,
    }


def _log_ai_call(record: dict) -> None:
    """Append one JSON line to logs/ai_calls_YYYY-MM-DD.jsonl (RF-021, spec §8.3)."""
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = _LOGS_DIR / f"ai_calls_{date_str}.jsonl"
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _try_model(model_id: str, system: str, user: str) -> ChatCompletion | None:
    """Try one model with 429 retry (max 2 per spec §12) + validation retry (max 1 per spec §9.4)."""
    rate_limit_retries = 0
    validation_retry_used = False
    prompt_hash = _prompt_hash(system, user)
    while True:
        print(
            f"[ai_client] attempt model={model_id} rl_retry={rate_limit_retries} "
            f"val_retry_used={validation_retry_used}",
            file=sys.stderr,
        )
        start = time.perf_counter()
        try:
            response = call_model(model_id, system, user, timeout=30)
        except RateLimitError:
            latency_ms = int((time.perf_counter() - start) * 1000)
            _log_ai_call(
                _ai_call_record(
                    model_id, prompt_hash, latency_ms, None, False,
                    {"format": None, "utf8": None}, rate_limit_retries, "rate_limited",
                )
            )
            if rate_limit_retries < 2:
                print(
                    f"[ai_client] 429 from {model_id}, backoff 30s "
                    f"(retry {rate_limit_retries + 1}/2)",
                    file=sys.stderr,
                )
                _sleep(30)
                rate_limit_retries += 1
                continue
            print(
                f"[ai_client] 429 after 2 retries on {model_id}, switching",
                file=sys.stderr,
            )
            return None
        except (APITimeoutError, TimeoutError):
            latency_ms = int((time.perf_counter() - start) * 1000)
            _log_ai_call(
                _ai_call_record(
                    model_id, prompt_hash, latency_ms, None, False,
                    {"format": None, "utf8": None}, rate_limit_retries, "timeout",
                )
            )
            print(f"[ai_client] timeout on {model_id}, switching", file=sys.stderr)
            return None
        except APIError as exc:
            latency_ms = int((time.perf_counter() - start) * 1000)
            _log_ai_call(
                _ai_call_record(
                    model_id, prompt_hash, latency_ms, None, False,
                    {"format": None, "utf8": None}, rate_limit_retries, "api_error",
                )
            )
            print(
                f"[ai_client] APIError on {model_id}: {type(exc).__name__}, switching",
                file=sys.stderr,
            )
            return None

        latency_ms = int((time.perf_counter() - start) * 1000)
        usage = None
        if response.usage is not None:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
            }
        content = response.choices[0].message.content or ""
        ok, parsed = validator_format(content)
        if not ok:
            _log_ai_call(
                _ai_call_record(
                    model_id, prompt_hash, latency_ms, usage, False,
                    {"format": False, "utf8": None}, rate_limit_retries, "validation_failed",
                )
            )
            if not validation_retry_used:
                print(
                    f"[ai_client] validator_format fail on {model_id}, retry 1/1",
                    file=sys.stderr,
                )
                validation_retry_used = True
                continue
            print(
                f"[ai_client] validator_format fail again on {model_id}, switching",
                file=sys.stderr,
            )
            return None

        ok, err = validator_utf8_encoding(parsed)
        if not ok:
            _log_ai_call(
                _ai_call_record(
                    model_id, prompt_hash, latency_ms, usage, True,
                    {"format": True, "utf8": False}, rate_limit_retries, "validation_failed",
                )
            )
            if not validation_retry_used:
                print(
                    f"[ai_client] validator_utf8 fail on {model_id}: {err}, retry 1/1",
                    file=sys.stderr,
                )
                validation_retry_used = True
                continue
            print(
                f"[ai_client] validator_utf8 fail again on {model_id}, switching",
                file=sys.stderr,
            )
            return None

        _log_ai_call(
            _ai_call_record(
                model_id, prompt_hash, latency_ms, usage, True,
                {"format": True, "utf8": True}, rate_limit_retries, "success",
            )
        )
        print(f"[ai_client] success on {model_id}", file=sys.stderr)
        return response


def get_suggestions_with_fallback(system: str, user: str) -> ChatCompletion:
    """Call chain with 429 backoff+retry and validation retry; switch on exhaustion (M3/T28-T29)."""
    chain = _chain_from_env()
    for model_id in chain:
        result = _try_model(model_id, system, user)
        if result is not None:
            return result
    raise RuntimeError(f"AI chain exhausted after trying {len(chain)} models")
