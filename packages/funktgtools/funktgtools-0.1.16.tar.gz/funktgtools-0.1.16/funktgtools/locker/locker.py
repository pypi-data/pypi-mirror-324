from aiogram.types import Message
from aiogram import Bot
import asyncio
from loguru import logger

class Locker:
    def __init__(self):
        self.user_buttons = {}
        self.user_locks = {}
        
    async def del_entry(self, user_id: int):
        """Deletes user_id / last_message entry from the game locks

        Args:
            user_id (int): telegram user id 
        """
        del self.user_locks[user_id]
        
    async def save_last_message(self, user_id: int, message_id: int):
        """Saves {user_id : last_message} entry in game locks

        Args:
            user_id (int): telegram user id 
            message_id (int): telegram message id 
        """
        self.user_buttons[user_id] = message_id
        
    async def command_lock(self, message: Message):
        """_summary_

        Args:
            message (Message): Message Object With User Command

        Returns:
            user_id, move_forward, user_lock: 
                User ID, 
                if command is allowed to move forward,
                and lastly Lock object or None
        """
        user_id = message.from_user.id
        move_forward = False
        user_lock = None
        if user_id not in self.user_locks:
            self.user_locks[user_id] = asyncio.Lock()
            move_forward = True
            user_lock = self.user_locks[user_id]
        
        
        return user_id, move_forward, user_lock

    async def attempt_editing_message(
        self, 
        message: Message, 
        bot: Bot, 
        user_id: int
    ) -> None:
        """_summary_

        Args:
            message (Message): TG Message
            bot (Bot): Bot Object
            user_id (int): Telegram User ID
        """
        if user_id in self.user_buttons:
            try:
                await bot.edit_message_reply_markup(
                    chat_id=user_id, 
                    message_id=self.user_buttons[user_id], 
                    reply_markup=None
                )
            #except MessageNotModified:
                #await message.reply("You are trying to mess around ain't you?")
            except Exception as e:
                logger.debug(str(e))
            finally:
                del self.user_buttons[user_id]

        # Send an immediate acknowledgment
        await message.reply("Processing your request...")
        
LOCKER = Locker()
