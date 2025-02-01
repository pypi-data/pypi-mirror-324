from loguru import logger
from random import randint
from aiogram import Router, F, Bot
from aiogram.types import Message
from ..config import BotConfig
from .forwarding import forward_router

admin_router = Router(name="admin_router")
admin_router.include_router(forward_router)

@admin_router.message(
    (F.text.startswith('/dm')) & 
    (F.chat.func(lambda chat: chat.type == 'private'))
)
async def mass_dm(
    message: Message, bot: Bot, config: BotConfig
) -> None:
    """Sends Mass Dm to user base

    Args:
        message (Message): Telegram Message
        bot (Bot): Telegram Bot to send Messages from
        user_class (User): Your tortoise user class with tg_id attr
        admins (list): List of Admins
    """
    user_id = message.from_user.id
    # Check if the user is the owner
    if user_id in config.admins:
        text = message.text.replace("/dm", "")
        users = await config.user_class.filter()
        for i in users:
            try:
                await bot.send_message(i.tg_id, text, parse_mode="markdown")
            #except CantParseEntities as e:
                #await message.reply(e + "\n Check if you applied correct markdown")#print(e)
                #break
            #except ChatNotFound as e:
                #exception = f"{i.name} with ID {i.tg_id} has closed his DM with bot"
                #logger.info(exception)
                
            #except BotBlocked as e:
                #exception = f"@{i.name} with ID {i.tg_id} has blocked bot"
                #logger.info(exception)
                
            except Exception as e:
                logger.warning(e)
                await message.reply(str(e))

        await message.reply("Done bro")

@admin_router.message(
    (F.text.startswith('/user')) & 
    (F.chat.func(lambda chat: chat.type == 'private'))
)
async def user_base(
    message: Message,
    config: BotConfig,
) -> None:
    """User Base Info

    Args:
        message (Message): Tg Message
        user_class (User): Tortoise User Class
        admins (list): List of Game Admins
    """
    user_id = message.from_user.id
    # Check if the user is the owner
    if user_id not in config.admins:
        return
    splitted = message.text.split() 
    if len(splitted) == 1:
        users = await config.user_class.filter()
        text = f"{len(users)} registered users.\n"
        #names = [f"\n´{user.name.replace('_', '\_')}`" for user in users]
        for user in users:
            name = user.name#.replace("_", "\_")
            text += f"\n`{name}`"
    elif len(splitted) == 2:
        user = await config.user_class.get_or_none(name=splitted[1])
        if not user:
            text = f"No user found with {splitted[1]} name..."
        else:
            text = await user.show_data()
            text += f"\nUser ID: {user.tg_id}"
    await message.reply(text, parse_mode = "markdown")

@admin_router.message(
    (F.text.startswith('/random')) & 
    (F.chat.func(lambda chat: chat.type == 'private'))
)
async def random_user(
    message: Message, 
    config: BotConfig
) -> None: 
    if message.from_user.id not in config.admins:
        return
    
    users = await config.user_class.filter()

    selected = randint(0, len(users)-1)
    await message.reply(f"1 Random user was selected:\n@{users[selected].name}")


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