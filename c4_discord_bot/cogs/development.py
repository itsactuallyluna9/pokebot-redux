from typing import Optional
from discord.ext.commands import Cog, Bot, command
from discord import Interaction, ui, TextStyle
from time import perf_counter


async def aexec(code, **kwargs):
    # Don't clutter locals
    locs = {}
    # Restore globals later
    globs = globals().copy()
    args = ", ".join(list(kwargs.keys()))
    exec(f"async def func({args}):\n    " + code.replace("\n", "\n    "), {}, locs)
    # Don't expect it to return from the coro.
    result = await locs["func"](**kwargs)
    try:
        globals().clear()
        # Inconsistent state
    finally:
        globals().update(**globs)
    return result


class EvalModal(ui.Modal, title="Eval"):
    code = ui.TextInput(
        label="Code",
        placeholder="Enter code here",
        min_length=1,
        max_length=2000,
        style=TextStyle.long,
    )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message("Evaluating...")
        try:
            result = await aexec(self.code.value, interaction=interaction)
            await interaction.edit_original_response(content=f"Result: {result}")
        except Exception as e:
            await interaction.edit_original_response(content=f"Error: {e}")


class Development(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def reload_extensions(self, interaction: Interaction, module: Optional[str]):
        """Reloads all extensions or a specific extension.

        Args:
            module (Optional[str]): The module to reload.
        """
        await interaction.response.defer(ephemeral=True)
        if module:
            try:
                await self.bot.reload_extension(module)
                await interaction.followup.send("Reloaded!")
            except Exception as e:
                await interaction.followup.send(f"Error: {e}")
        else:
            # reload everything
            extensions = list(self.bot.extensions.keys())
            failed = []
            for extension in extensions:
                try:
                    await self.bot.reload_extension(extension)
                except Exception as e:
                    failed.append((extension, e))
            if failed:
                await interaction.followup.send(
                    f"Failed to reload {len(failed)} extensions!\n"
                    + "\n".join([f"* {ext}: {e}" for ext, e in failed])
                )
            else:
                await interaction.followup.send(
                    f"Reloaded all {len(extensions)} extensions!"
                )

    @command()
    async def load_extension(self, interaction: Interaction, module: str):
        """Loads an extension.

        Args:
            module (str): The module to load.
        """
        await interaction.response.defer(ephemeral=True)
        try:
            await self.bot.load_extension(module)
            await interaction.followup.send("Loaded!")
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

    @command()
    async def reload_commands(self, interaction: Interaction):
        """Reloads the commands."""
        await interaction.response.defer(ephemeral=True)
        await self.bot.sync_tree()
        await interaction.followup.send("Reloaded commands!")

    @command()
    async def async_eval(self, interaction: Interaction):
        """Evaluates potentially async code. Add `return` to recieve the result."""
        await interaction.response.send_modal(EvalModal())


async def setup(bot):
    await bot.add_cog(Development(bot))
