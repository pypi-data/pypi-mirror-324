"""from aiogram import types, Dispatcher, Bot
from aiogram.methods.set_message_reaction import SetMessageReaction
from aiogram.types import ReactionTypeEmoji

async def react_to_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("You need to reply to a message to react to it.")
        return

    emoji = "😁"  # The emoji to react with
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id

    reaction = ReactionTypeEmoji(emoji=emoji)
    await message.bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=[reaction])

    await message.reply("Reaction added!")
"""