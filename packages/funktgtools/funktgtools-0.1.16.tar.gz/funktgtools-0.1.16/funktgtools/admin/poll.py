from aiogram import types

async def send_poll(message: types.Message):
    args = message.text.split('\n')
    if len(args) < 3:
        await message.reply("You need to provide a poll question and at least two choices.")
        return

    question = args[0].replace('/poll ', '')
    choices = args[1:]

    await message.bot.send_poll(
        chat_id=message.chat.id, 
        question=question, 
        options=choices, 
        is_anonymous=False)
