from aiogram import types, Bot
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from ..config import BotConfig





forward_router = Router(name="forward_router")

@forward_router.message(
    (F.text.startswith('/forward')) & 
    (F.chat.func(lambda chat: chat.type == 'private'))
)
async def dev_calls_forward_message(message: Message, bot: Bot, config: BotConfig):
    user_id = message.from_user.id
    if not message.reply_to_message:
        await message.reply("You need to reply to a message to use this command.")
        return

    args = message.text.split()
    if len(args) < 2:
        await message.reply("You need to provide a keyword to indicate the target chat.")
        return
    if user_id not in config.admins:
        return
    
    await dev_forward(message, bot, config, True if len(args) == 3 and args[2].lower() == "true" else False)
    
    
async def welcome_user(
    bot: Bot, 
    message_text: str, 
    keyword: str,
    config: BotConfig
) -> Message:
    
    await bot.send_message(
        config.owner, 
        message_text,
        parse_mode="markdown"
    )
    return await bot.send_message(
        config.chats[keyword], 
        message_text,
        parse_mode="markdown",
        message_thread_id=config.threads[keyword] if keyword in config.threads.keys() else None
    )
    
async def dev_forward(message: types.Message, bot: Bot, config: BotConfig, pin: bool=False):
    user_id = message.from_user.id
    
    # Check if the user is the owner
    
    forwarded = await forward_message(message, bot, config)
    
    if pin and forwarded:
        return await pin_message(bot, forwarded.chat.id, forwarded.message_id)
    if not forwarded:
        return await message.reply("Unable to forward")

async def forward_message(message: types.Message, bot: Bot, config: BotConfig):
    
    args = message.text.split()
    keyword = args[1]
    chat_id = config.chats.get(keyword, None)
    thread = config.threads.get(keyword, None)
    if not chat_id:
        await message.reply("Invalid keyword provided.")
        return

    return await bot.forward_message(
        chat_id, 
        message.chat.id, 
        message.reply_to_message.message_id,
        message_thread_id=thread)

async def pin_message(bot: Bot, chat_id: int, message_id: int):
    await bot.pin_chat_message(chat_id, message_id)         
