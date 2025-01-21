from discord.ext.commands import Cog, Bot, command
from discord import Interaction, Embed, app_commands
from asyncio import subprocess
from platform import system, release, python_version
import shutil


class NeoFetch(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def neofetch(self, interaction: Interaction):
        """Displays bot information."""
        embed = Embed(
            title="C4 Discord Bot",
            url="https://github.com/CornellCollegeComputingClub/discord-bot",
            color=0xFF40FF,
        )
        embed.add_field(name="OS", value=f"{system()} {release()}")
        embed.add_field(name="Python Version", value=python_version(), inline=True)
        
        git_path = shutil.which("git") or "/usr/bin/git"
        git_command = f"{git_path} log -1 --pretty=format:'%h (%s)'"
        process = await subprocess.create_subprocess_shell(
            git_command, stdout=subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        commit = stdout.decode().strip()
        embed.add_field(name="Commit", value=commit)

        # authors: get top contributors
        git_command = f"{git_path} shortlog -s -n"
        process = await subprocess.create_subprocess_shell(
            git_command, stdout=subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        authors = stdout.decode().strip().split("\n")
        # top authors = "author1, author2, author3"
        top_authors = ", ".join([author.split("\t")[1] for author in authors[:3]])
        tail = ""
        if len(authors) > 3:
            tail = f" and {len(authors) - 3} more"

        embed.set_author(
            name=f"Created by {top_authors}{tail}",
            url="https://github.com/CornellCollegeComputingClub/discord-bot/graphs/contributors",
            icon_url="https://avatars.githubusercontent.com/u/119377910?s=200&v=4",
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(NeoFetch(bot))
