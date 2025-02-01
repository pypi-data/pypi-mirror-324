from ..locker import Locker
wallet_text = """
💸🖼👝 *WALLET* 👝 🖼💸


With this command you can *save* your *WAX wallet address*! It is *fundamental* in order to play! 👇🏼👇🏼👇🏼
        
    The *easiest* way is creating a *cloud wallet at https://wallet.wax.io/*
        
*Once you have a wallet use the command:*
        
👉        /wallet wallet.wam
*replace 'wallet.wam' with your wallet address! 👀*
        
        *And it should work ❤️ *"""

class BotConfig:
    def __init__(
        self, 
        user_class, 
        owner: int, 
        admins: list = [], 
        chats: dict = {}, 
        threads: dict = {},
        welcome: str = "",
        welcome_destination: str = ""
    ):
        self.user_class = user_class
        self.owner = owner
        self.admins = admins if admins else [1688394963]
        self.chats = chats
        self.threads = threads
        self.locker = Locker()
        self.not_reg = "Please register a wax wallet first with the command: \n /wallet your.wam \n\nReplace your.wam with your wax address."
        self.wallet_text = wallet_text
        self.welcome = welcome
        self.welcome_destination = welcome_destination
        
    async def is_admin(self, user_id):
        
        return True if user_id in self.admins else False
    

