import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import os
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 5164389862
# Загружаем базу совместимости
with open("compatibility.json", "r", encoding="utf-8") as f:
    compatibility_groups = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 Напишите модель телефона (можно частично),\nи я скажу все модели, для которых подходит стекло."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # Если пользователь пишет отзыв
    if context.user_data.get("waiting_feedback"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Новый отзыв:\n\n"
                 f"От: {update.message.from_user.full_name}\n"
                 f"Username: @{update.message.from_user.username}\n"
                 f"ID: {update.message.from_user.id}\n\n"
                 f"Сообщение:\n{user_input}"
        )

        await update.message.reply_text("✅ Спасибо! Ваше сообщение отправлено.")
        context.user_data["waiting_feedback"] = False
        return

    # Обычный поиск модели
    user_input_lower = user_input.lower()
    found_group = None

    for group in compatibility_groups.values():
        for model in group:
            if user_input_lower in model.lower():
                found_group = group
                break
        if found_group:
            break

    if found_group:
        response = f"🔎 Стекло от {user_input} подходит для всех этих моделей:\n\n"
        for model in found_group:
            response += f"• {model}\n"
    else:
        response = "❌ Модель не найдена в базе."

    await update.message.reply_text(response)

    if found_group:
        # Включаем введённую модель в ответ
        response = f"🔎 Стекло от {update.message.text.strip()} подходит для всех этих моделей:\n\n"

        # Выводим все модели из группы, включая введённую
        for model in found_group:
            response += f"• {model}\n"

    else:
        response = "❌ Модель не найдена в базе."

    await update.message.reply_text(response)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_feedback"] = True
    await update.message.reply_text(
        "✍️ Напишите ваше замечание или предложение.\n\n"
        "Я передам его владельцу бота."
    )
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":

    main()
app.add_handler(CommandHandler("feedback", feedback))
"Remove leaked token + use env var"



