from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime, timedelta
from ..config import BotConfig
from tortoise.models import Q
from loguru import logger
from funktgtools import welcome_user

wallet_router = Router(name="wallet_router")


@wallet_router.message(
    (F.text.startswith('/wallet')) & 
    (F.chat.func(lambda chat: chat.type == 'private'))
)
async def bot_wallet_dialogue(message, config: BotConfig):
    await wallet_dialog(message, config)



async def wallet_dialog(message: Message, config: BotConfig):
    tg_username = message.from_user.username.replace("_", "\_")
    user_id = message.from_user.id
    logger.info(f"{tg_username}: '{message.text}'")
    now = datetime.now()
    twenty_four_hours_ago = now - timedelta(hours=24)
    User = config.user_class
    if len(message.text.split()) == 1:
        
        return await message.reply(config.wallet_text, parse_mode="Markdown", disable_web_page_preview=True
        )
    if len(message.text.split()) > 2:
        return await message.reply(f"@{tg_username} you are doing something wrong!")
    if len(message.text.split()[1]) > 12:
        return await message.reply(f"@{tg_username} you entered an invalid wallet!")
    if len(message.text.split()) == 2:
        address = message.text.split()[1]
        player = await User.filter(Q(tg_id=user_id) | Q(wallet=address)).first()

        if player:
            user = await User.get_or_none(wallet=address)
            if user and user_id == user.tg_id:
                await message.reply(f"{message.from_user.username}you are on the list already!")
            elif user and user.tg_id != user_id:
                await message.reply(f"{message.from_user.username}this wallet address belongs to another user!")
        else:
            logger.info(
                f"Registering {tg_username} ({user_id}) with wallet {address} in the DB."
            )
            user = await User.create(name=message.from_usr.username, tg_id=user_id, wallet=address, last_claim = twenty_four_hours_ago.timestamp())
            
            await user.procriate()
            await message.reply(
                f"Nice to know you, @{tg_username}! Your wallet address was saved to the DataBase.\n\nPlease run /claim to update your holdings and claim melting points!",
            )
            await welcome_user(
                bot=config.bot, 
                message_text=config.welcome.format(user),
                keyword=config.welcome_destination,
                config = config)