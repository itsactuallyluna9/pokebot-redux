import discord
from discord.ext import commands
from os import environ


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def setup_hook(self):
        await self.load_cogs()
        await self.sync_tree()

    async def sync_tree(self):
        # must be in development mode to sync locally
        if environ.get("ENV") == "development":
            if environ.get("TEST_GUILD_ID") is None:
                print(
                    "TEST_GUILD_ID not set! Can't do fast sync. Falling back to globally syncing..."
                )
                await self.tree.sync()
            TEST_GUILD = discord.Object(id=environ.get("TEST_GUILD_ID"))
            self.tree.copy_global_to(guild=TEST_GUILD)
            await self.tree.sync(guild=TEST_GUILD)
        else:
            await self.tree.sync()

    async def load_cogs(self):
        if environ.get("ENV") == "development":
            await self.load_extension("c4_discord_bot.cogs.development")
        await self.load_extension("c4_discord_bot.cogs.neofetch")


intents = discord.Intents.all()
client = Client(
    "!!!", intents=intents
)  # !!! is our prefix. since we're using slash commands, this is not used. it's still needed, though.
