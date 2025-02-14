from discord import app_commands, Interaction
from discord.ext import commands
from typing import Optional
import json

from .pokebot_evolved import PokebotEvolved

class PokeCog(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command()
    @app_commands.describe(name='Enter a name to generate information for (optional)')
    async def generate(self, interaction: Interaction, name: Optional[str]=None):
        #entry = await PokebotEvolved.generateFullEntry(prompt=name)
        entry = PokebotEvolved().nameTypeStat(prompt=name)
        new_entry = list()
        new_entry.append(entry[0])
        new_entry.append(entry[1])
        new_entry.append(list(int(x) for x in entry[2]))
        out = json.dumps(new_entry)
        await interaction.response.send_message(out)

async def setup(bot):
    await bot.add_cog(PokeCog(bot))
