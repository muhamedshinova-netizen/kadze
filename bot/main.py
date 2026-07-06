import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from database import can_generate, increment_generation
from tasks import generate_animation
import logging

logging.basicConfig(level=logging.INFO)

user_selections = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    webapp_url = os.getenv("WEBAPP_URL", "https://example.com")
    keyboard = [[InlineKeyboardButton("🎨 Создать анимацию", web_app=WebAppInfo(url=webapp_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я Тёплый Кадр – превращаю фото в уютную анимацию ✨\nНажми кнопку ниже, чтобы начать!",
        reply_markup=reply_markup
    )

async def handle_webapp_data(update: Update, context):
    data = json.loads(update.message.web_app_data.data)
    user_id = update.effective_user.id
    user_selections[user_id] = {
        'category': data.get('category', 'portrait'),
        'style': data.get('style', 'default')
    }
    await update.message.reply_text("Теперь отправь мне фото, и я применю выбранный стиль!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not can_generate(user_id):
        await update.message.reply_text("Сегодня лимит бесплатных генераций исчерпан. Попробуй завтра или оформи подписку.")
        return

    selection = user_selections.get(user_id, {'category': 'portrait', 'style': 'default'})
    photo_file = await update.message.photo[-1].get_file()
    photo_url = photo_file.file_path

    msg = await update.message.reply_text("✨ Генерирую анимацию... Подожди до 30 секунд.")
    try:
        video_path = generate_animation(photo_url, selection['category'], selection['style'], user_id)
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="Вот твой тёплый кадр! 💛"
            )
        increment_generation(user_id)
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Ой, что-то пошло не так. Попробуй ещё раз позже.")
    finally:
        await msg.delete()
        if 'video_path' in locals() and os.path.exists(video_path):
            os.unlink(video_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    app.run_polling()
