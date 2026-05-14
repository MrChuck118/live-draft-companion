"""OpenRouter SDK client setup, single-model call, fallback chain and validation retry (M3/T26-T29)."""

import os
import sys
import time

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


def _try_model(model_id: str, system: str, user: str) -> ChatCompletion | None:
    """Try one model with 429 retry (max 2 per spec §12) + validation retry (max 1 per spec §9.4)."""
    rate_limit_retries = 0
    validation_retry_used = False
    while True:
        try:
            print(
                f"[ai_client] attempt model={model_id} rl_retry={rate_limit_retries} "
                f"val_retry_used={validation_retry_used}",
                file=sys.stderr,
            )
            response = call_model(model_id, system, user, timeout=30)
        except RateLimitError:
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
            print(f"[ai_client] timeout on {model_id}, switching", file=sys.stderr)
            return None
        except APIError as exc:
            print(
                f"[ai_client] APIError on {model_id}: {type(exc).__name__}, switching",
                file=sys.stderr,
            )
            return None

        content = response.choices[0].message.content or ""
        ok, parsed = validator_format(content)
        if not ok:
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
