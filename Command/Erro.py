import discord
from discord import app_commands


class Erro():
    def __init__(self, client):
        self.client = client
        
    
    def setup(self):
        @self.client.tree.error
        async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
            if isinstance(error, app_commands.errors.CommandOnCooldown):
                await interaction.response.send_message(f'Command "{interaction.command.name}" is on cooldown, you can use it in {round(error.retry_after, 2)} seconds.', ephemeral=True)   
