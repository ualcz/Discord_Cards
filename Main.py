import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from config import *
from Command.CommandCard import CommandCard
from Command.Erro import Erro
from Database.data import Base


# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN2')

data=Base()

class MyClient(discord.Client):
    def __init__(self, *,db, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.database = db

    async def setup_hook(self):
        await self.tree.sync()
       

intents = discord.Intents.default()
client = MyClient(intents=intents,db=data)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')



# Configure and setup Card
Card_command= CommandCard(client=client)
Card_command.setup()

# Configure and setup Erro
Erro= Erro(client=client)
Erro.setup()


client.run(DISCORD_TOKEN)