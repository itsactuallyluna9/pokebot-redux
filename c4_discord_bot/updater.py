import discord
from discord.ext.commands import Bot
from discord.ext.commands.errors import ExtensionNotLoaded
from asyncio import subprocess

async def do_auto_update(bot: Bot):
    # basic process:
    # - do we have updates (via git)?
    # - - if not, exit
    # - pull updates
    # - if anything not in cogs has updated, print (because im not sure how to handle that yet)
    # - reload cogs
    # - - if anything fails, print
    
    # check for updates
    git_command = "git fetch"
    process = await subprocess.create_subprocess_shell(git_command, stdout=subprocess.PIPE)
    stdout, _ = await process.communicate()
    if not stdout:
        return  # no updates
    
    # we have updates!

    # set bot status and activity
    await bot.change_presence(activity=discord.Game(name="Updating..."), status=discord.Status.idle)

    # log current commit
    git_command = "git log -1 --pretty=format:'%h'"
    process = await subprocess.create_subprocess_shell(git_command, stdout=subprocess.PIPE)
    stdout, _ = await process.communicate()
    previous_commit = stdout.decode().strip()

    git_command = "git pull"
    process = await subprocess.create_subprocess_shell(git_command, stdout=subprocess.PIPE)
    stdout, _ = await process.communicate()

    # what did we update?
    # we need to also keep track of added/modified/deleted so we can use the correct method later
    git_command = f"git diff --name-status {previous_commit} HEAD"
    process = await subprocess.create_subprocess_shell(git_command, stdout=subprocess.PIPE)
    stdout, _ = await process.communicate()
    changes = {}
    for change in stdout.decode().strip().split("\n"):
        status, file = change.split("\t")
        if file.endswith(".md") or file in (".gitignore", ".env.example"):
            continue

        changes[file] = status
    
    # alright, do we have any of out other python files in the changes?
    if not(all("cogs" in file for file in changes.keys())):
        print("Non-cog files have been updated!!!")
    
    # reload cogs
    for change in changes:
        if "cogs" not in file:
            continue
        extension = change.replace("/", ".").replace(".py", "")
        if changes[change] == "D":
            try:
                bot.unload_extension(extension)
            except:
                # ignore errors, because it's either not found or not loaded.
                # so like, who cares?
                pass
        elif changes[change] == "M":
            try:
                try:
                    bot.reload_extension(extension)
                except ExtensionNotLoaded:
                    # if it's not loaded, load it
                    bot.load_extension(extension)
            except Exception as e:
                print(f"Failed to reload {extension} due to {e}")
        elif changes[change] == "A":
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f"Failed to load {extension} due to {e}")
        else:
            print(f"Unknown status {changes[change]} for {change}")
    
    # set bot status and activity
    await bot.change_presence(activity=None, status=discord.Status.online)
