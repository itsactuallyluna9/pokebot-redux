from discord import app_commands, Interaction, Embed
from discord.ext import commands
from typing import Optional

class PokeCog(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.state = None
    
    @app_commands.command()
    @app_commands.describe(name='Enter a name to generate information for (optional)')
    async def generate(self, interaction: Interaction, name: Optional[str]=None):
        if not self.state:
            # lazy load
            from .pokebot_evolved import PokebotEvolved
            self.state = PokebotEvolved()
        
        entry = self.state.generateFullEntry(prompt=name, print_to_console=False)
        embed = self.make_embed(entry)
        await interaction.response.send_message(embed=embed)
    
    def make_embed(self, entry: dict):
        embed = Embed(title=entry['name'], description=entry['description'])
        if entry['category'] is not None:
            embed.add_field(name='Category', value=entry['category'])
        embed.add_field(name='Type', value=entry['type1'] + (', ' + entry['type2'] if entry['type2'] else ''))
        embed.add_field(name='Stats', value=f"HP: {entry['hp']}\nAttack: {entry['atk']}\nDefense: {entry['def']}\nSpecial Attack: {entry['spatk']}\nSpecial Defense: {entry['spdef']}\nSpeed: {entry['speed']}")
        embed.set_author(name='Generated using Pokebot Evolved')
        return embed

async def setup(bot):
    await bot.add_cog(PokeCog(bot))
