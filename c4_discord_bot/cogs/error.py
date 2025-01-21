from discord.ext.commands import Cog, Bot
from discord import Interaction, DiscordException, Embed
import traceback

class Error(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.event

    @Cog.listener()
    async def on_application_command_error(interaction: Interaction, error: DiscordException):
        # this is just so don't silently fail to the user
        # if an error occurs, you should try to handle it locally! this is a basically a last-resort.
        embed = Embed(
            title="Error",
            color=0xFF0000,
        )

        embed.description = f"An error occurred: {error}"
        embed.add_field(name="Traceback", value=f"```py\n{traceback.format_exc()}```")

        await interaction.response.send_message(embed=embed, ephemeral=True)

        raise error


async def setup(bot):
    await bot.add_cog(Error(bot))
