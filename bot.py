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


def get_keyboard(chat_id: int):
    count = dinners.get(chat_id, START_COUNT)

    buttons = []

    # кнопка заказа минта
    if count > 0:
        buttons.append(
            [InlineKeyboardButton("🍽 Заказать минт", callback_data="order")]
        )

    # кнопка "купить ещё"
    buttons.append(
        [InlineKeyboardButton("🍷 Купить ещё", callback_data="buy_more")]
    )

    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    dinners[chat_id] = START_COUNT

    text = (
        "С днём рождения, моя нежная Любовь!\n"
        "Спасибо что есть в моей жизни.\n"
        "Хоть ты и не мой, но мне легче жить в этом мире, зная, что где-то ты, хоть и далеко, но рядом.\n"
        "Очень ценю и уважаю тебя, мой Воин 🔥\n\n"
        "🎉 Поздравляем!\n\n"
        "Вам подарено 10 минтов 🍽\n"
        "Нажимайте кнопку ниже, чтобы заказать минт."
    )

    await update.message.reply_text(
        text,
        reply_markup=get_keyboard(chat_id)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = query.data

    count = dinners.get(chat_id, START_COUNT)

    if data == "order":
        if count <= 0:
            await query.edit_message_text(
                "У вас больше не осталось минтов 😢",
                reply_markup=get_keyboard(chat_id)
            )
            return

        count -= 1
        dinners[chat_id] = count

        if count > 0:
            text = (
                f"🍽 Минт заказан!\n"
                f"Осталось минтов: {count}"
            )
        else:
            text = (
                "🍽 Минт заказан!\n\n"
                "У вас закончились все минты 🎉"
            )

        await query.edit_message_text(
            text,
            reply_markup=get_keyboard(chat_id)
        )

    elif data == "buy_more":
        await query.answer()
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
