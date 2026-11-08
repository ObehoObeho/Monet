# 🎨 Monet

Asistente personal estilo Jarvis. Versión 0.1: bot de Telegram con voz.

## Instalación en Windows (Galaxy Book)

1. Instala **Python 3.12** desde https://www.python.org/downloads/ (marca "Add Python to PATH").
2. Descarga este repositorio (botón verde **Code → Download ZIP**) y descomprímelo.
3. Abre la carpeta, clic derecho → **Abrir en Terminal**, y ejecuta:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env
   notepad .env
   ```
4. En el Bloc de notas pega tu `TELEGRAM_TOKEN` y guarda.
5. Arranca a Monet:
   ```
   python -m monet.bot
   ```
6. En Telegram escríbele `/start` a tu bot. Te dirá tu ID: ponlo en `OWNER_ID` dentro de `.env`, guarda, cierra Monet (Ctrl+C) y vuelve a arrancarlo.

## Comandos
- `/voz` – activar/desactivar respuestas con voz
- `/olvidar` – borrar la conversación
- `/id` – ver tu ID

## Seguridad
- `.env` tiene tus claves: **nunca** lo compartas ni lo subas a GitHub.
- Solo el `OWNER_ID` puede hablar con Monet.
