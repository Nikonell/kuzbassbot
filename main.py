from aiogram import Bot, Dispatcher, executor, types
import config
import time

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)
suggestion_times = {}


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Я вас категорически приветствую! Чтобы отправить новость или предложение в ИА \"Кузбасс\", напишите /suggest <текст>.")


@dp.message_handler(content_types=["text", "photo", "video", "document"])
async def suggest_command(message: types.Message):
    if (not message.text or not message.text.startswith("/suggest")) and (not message.caption or not message.caption.startswith("/suggest")):
        return
    mtext = message.text if message.text else message.caption
    suggestion = mtext.replace("/suggest", "").strip()
    if suggestion == "":
        await message.answer("Нельзя отправить пустое предложение! Используйте /suggest <текст>.")
    elif len(suggestion) < 10:
        await message.answer("Предложение должно быть не меньше 10 символов.")
    elif len(suggestion) > 1000:
        await message.answer("Предложение должно быть не больше 1000 символов.")
    elif time.time() - suggestion_times.get(message.from_user.id, 0) < 600:
        await message.answer("Предложения можно отправлять не чаще чем раз в 10 минут.")
    else:
        op_message = await bot.send_message(config.MODER_CHAT_ID, f"Предложение от {message.from_user.full_name}. Отправлено {message.date.strftime('%d.%m.%Y %H:%M')}.\n{suggestion}")
        if message.photo:
            await op_message.reply_photo(message.photo[-1].file_id)
        if message.video:
            await op_message.reply_video(message.video.file_id)
        if message.document:
            await op_message.reply_document(message.document.file_id)
        suggestion_times[message.from_user.id] = time.time()
        await message.answer("Предложение успешно отправлено.")


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
