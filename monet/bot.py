import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from . import brain, voice

load_dotenv()
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger("monet")

OWNER_ID = os.getenv("OWNER_ID", "").strip()
voice_on = {"enabled": False}


def is_owner(update: Update) -> bool:
    return bool(OWNER_ID) and str(update.effective_user.id) == OWNER_ID


async def guard(update: Update) -> bool:
    """Solo el dueño puede usar a Monet."""
    if is_owner(update):
        return True
    if not OWNER_ID:
        await update.message.reply_text(
            f"Hola. Tu ID es {update.effective_user.id}. Ponlo en OWNER_ID dentro de .env "
            "y reinicia a Monet.")
    else:
        log.warning("Acceso denegado a %s", update.effective_user.id)
    return False


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if await guard(update):
        await update.message.reply_text(
            "🎨 Monet en línea, señor.\n/voz – activar/desactivar respuestas con voz\n"
            "/olvidar – borrar la conversación\n/id – ver tu ID")


async def my_id(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Tu ID de Telegram es: {update.effective_user.id}")


async def toggle_voice(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if await guard(update):
        voice_on["enabled"] = not voice_on["enabled"]
        estado = "activada 🗣️" if voice_on["enabled"] else "desactivada 💬"
        await update.message.reply_text(f"Voz {estado}, señor.")


async def forget(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if await guard(update):
        brain.forget(update.effective_chat.id)
        await update.message.reply_text("Memoria de esta conversación borrada, señor.")


async def chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await guard(update):
        return
    await ctx.bot.send_chat_action(update.effective_chat.id, "typing")
    answer = brain.think(update.effective_chat.id, update.message.text)
    await update.message.reply_text(answer)
    if voice_on["enabled"]:
        path = await voice.speak(answer)
        try:
            with open(path, "rb") as f:
                await update.message.reply_audio(f, title="Monet")
        finally:
            os.remove(path)


def main():
    token = os.getenv("TELEGRAM_TOKEN", "").strip()
    if not token:
        raise SystemExit("Falta TELEGRAM_TOKEN en el archivo .env")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", my_id))
    app.add_handler(CommandHandler("voz", toggle_voice))
    app.add_handler(CommandHandler("olvidar", forget))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    log.info("Monet en línea. Ctrl+C para apagar.")
    app.run_polling()


if __name__ == "__main__":
    main()
