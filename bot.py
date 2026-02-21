import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7972473497:AAHr7fN3GR5cKLilr7UsGEL5EQSuEaHeQVg"

# Загружаем базу совместимости
with open("compatibility.json", "r", encoding="utf-8") as f:
    compatibility_groups = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 Напишите модель телефона (можно частично),\nи я скажу все модели, для которых подходит стекло."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()
    found_group = None

    # Ищем частичное совпадение
    for group in compatibility_groups.values():
        for model in group:
            if user_input in model.lower():
                found_group = group
                break
        if found_group:
            break

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

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()