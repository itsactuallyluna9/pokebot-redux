from discord import app_commands, Interaction
from discord.ext import commands
from typing import Optional
import json

from pokebot_evolved import PokebotEvolved

class PokeCog(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command()
    @app_commands.describe(name='Enter a name to generate information for (optional)')
    async def generate(self, interaction: Interaction, name: Optional[str]=None):
        #entry = await PokebotEvolved.generateFullEntry(prompt=name)
        entry = await PokebotEvolved.nameTypeStat(prompt=name)
        out = json.dumps(entry)
        await interaction.response.send_message(out)