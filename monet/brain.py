import os
from collections import defaultdict, deque

from .personality import SYSTEM_PROMPT

_history = defaultdict(lambda: deque(maxlen=20))  # memoria corta por chat
_client = None


def _get_client():
    global _client
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        return None
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(api_key=key)
    return _client


def think(chat_id: int, text: str) -> str:
    client = _get_client()
    if client is None:
        return ("Modo básico, señor: aún no tengo cerebro conectado (falta la clave de la API "
                f"de Claude). Recibí: \"{text}\"")
    hist = _history[chat_id]
    hist.append({"role": "user", "content": text})
    try:
        resp = client.messages.create(
            model=os.getenv("MONET_MODEL", "claude-haiku-5-5"),
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=list(hist),
        )
        answer = "".join(b.text for b in resp.content if b.type == "text").strip()
    except Exception as e:  # noqa: BLE001
        hist.pop()
        return f"Tuve un problema pensando, señor: {e}"
    hist.append({"role": "assistant", "content": answer})
    return answer


def forget(chat_id: int) -> None:
    _history.pop(chat_id, None)
