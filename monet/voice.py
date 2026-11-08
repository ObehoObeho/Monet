import os
import tempfile

import edge_tts


async def speak(text: str) -> str:
    """Convierte texto a voz (MP3) y devuelve la ruta del archivo."""
    voice = os.getenv("MONET_VOICE", "es-MX-JorgeNeural")
    fd, path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    await edge_tts.Communicate(text, voice).save(path)
    return path
