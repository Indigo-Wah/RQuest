'''
    Revolt Client
'''
from os import getenv
# import base64
import asyncio
import revolt
import aiohttp
from dotenv import load_dotenv

load_dotenv()


class Token():
    '''
        Secure Token Class
    '''

    def __init__(self):
        self._token:  str | None = None

    def set_token(self, token: str):
        '''
        Takes in a Str and encrpyts it before storing it
        '''
        if token is None or len(token) == 0:
            raise ValueError("Token cannot be None")
        # self._token = base64.b64encode(token)
        self._token = token

    def get_token(self) -> str:
        '''
        Returns the token as a string
        '''
        # return base64.b64decode(self._token)
        return self._token

    def is_token_set(self) -> bool:
        '''
        Checks if the token is set
        '''
        return self._token is not None


class Client(revolt.Client):
    '''
        Revolt Client Class
    '''

    def __init__(self, session: aiohttp.ClientSession, token: Token):
        super().__init__(session=session, token=token.get_token())

    async def on_ready(self) -> None:
        print(f"{self.user.name} is ready!")
        return await super().on_ready()

    async def on_message(self, message: revolt.Message) -> None:
        # Pull out the command keyword
        if not message.content.startswith("!"):
            return await super().on_message(message)

        # Capture first command keyword
        match message.content.split(" ")[0][1:].lower():
            case "ping":
                await message.channel.send("pong")
            case "task":
                # Capture second command keyword
                match message.content.split(" ")[1].lower():
                    case "math":
                        await message.channel.send("Math is hard")

        return await super().on_message(message)


async def main():
    '''
        Main Async Function
    '''
    token = Token()
    token.set_token(getenv("TOKEN"))
    async with aiohttp.ClientSession() as session:
        client = Client(session=session, token=token)
        await client.start()

if __name__ == "__main__":
    asyncio.run(main())
