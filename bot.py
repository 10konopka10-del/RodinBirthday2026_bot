from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = "8335949785:AAFYts7NRgIV8q3ScdAoMwbtSN1wdNuI1sE"

dinners = {}
START_COUNT = 10


def get_keyboard(count: int):
    buttons = []

    # кнопка заказа минтов
    if count > 0:
        buttons.append(
            [InlineKeyboardButton("🍽 Заказать минет", callback_data="order")]
        )

    # кнопка покупки ВСЕГДА есть
    buttons.append(
        [InlineKeyboardButton("🍷 Купить дополнительные услуги", callback_data="buy_more")]

    )

    return InlineKeyboardMarkup(buttons)


def get_final_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍷 Купить дополнительные услуги", callback_data="buy_more")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    dinners[chat_id] = START_COUNT

    text = (
        "😻С днём рождения, моя нежная Любовь!\n"
        "Спасибо что есть в моей жизни.\n"
        "Хоть ты и не мой, но мне легче жить в этом мире, зная, что где-то ты, хоть и далеко, но рядом.\n"
        "Очень ценю и уважаю тебя,мой Воин🔥\n\n"
        "🎉 Поздравляем!\n\n"
        "Вам подарено 10 минетов 🍽\n"
        "Нажимайте кнопку ниже, чтобы заказать минт и отправьте скриншот исполнителю для подтверждения заказа"
    )

    await update.message.reply_text(
        text,
        reply_markup=get_keyboard(dinners[chat_id])
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = query.data

    count = dinners.get(chat_id, START_COUNT)

    # заказ минта
    if data == "order":
        if count <= 0:
            await query.message.reply_text("У вас больше не осталось минетов 😢")
            await query.message.reply_text(
                "Если хотите продолжить — нажмите кнопку ниже 👇",
                reply_markup=get_final_keyboard()
            )
            return

        count -= 1
        dinners[chat_id] = count

        await query.message.reply_text("🍽 Минет заказан!")

        if count > 0:
            await query.message.reply_text(f"Осталось минтов: {count}")
        else:
            await query.message.reply_text(
                "У вас закончились все минеты 🎉"
            )

    # покупка услуг
    elif data == "buy_more":
        await query.message.reply_text(
            "🍷 Конечно можем договориться.\n"
            "Напишите нам, и мы обсудим детали 😉"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
