# How To Make a Command for the Bot

Hello! This guide will guide you in making your very own command for C4's Discord Bot! This guide only coveres the basics, but we will briefly mention some more advanced topics.

## Setting Up Your Environment

In order to work on the bot, you will first need to have Python 3.11 (or above), git, and poetry installed. Additionally, you will need a GitHub account so you can add your work later, a Discord account, and we recommend using VS Code to work on your code.

With the necessities out of the way, let's set up your environment!

First, you must fork the repository on GitHub. This will create a copy of the repository under your own GitHub account. To do this, just hit the `Fork` button in the top right corner, and follow the instructions.

Next, we must clone the repository to your computer. You may use a GUI if you have one, but we'll be using the command line for this guide.

```sh
luna (~) > cd Documents/Code
luna (~/D/Code) > git cline https://github.com/itsactuallyluna9/c4-discord-bot.git

luna (~/D/Code) > cd c4-discord-bot
luna (~/D/C/c4-discord-bot) > # we have our code!
```

We now have the code on our computer! We still have a bit of work to do, like installing all of our dependencies, and setting up a testing bot. For dependencies, this is easily accomplished by running the following command in the `c4-discord-bot` directory we just downloaded:

While we're here, we'll also make a copy of our environment file to fill in later.

```sh
$ poetry install
$ cp .env.example .env
```

(Note: we'll be using the `$` character to indicate a shell command from here on out!)

Next, we'll need to make ourselves a bot, and a little server to test the bot in.

First, let's make ourselves a server. To do this, go to Discord, scroll down and hit the `+` button (it should say `Add a Server`). Hit "Create My Own", "For me and my friends", and you can give it a name and hit Create!

Once you're there, make sure to keep a text channel around, you'll need it later.

While we're still in Discord, we'll want to grab the ID of the server we just made. We'll first need to enable Developer Mode (by going to Settings -> App Settings -> Advanced -> Developer Mode), and then right-clicking the server and hitting "Copy Server ID". This will copy a ID to your clipboard, keep track of it, we'll use it in a moment.

Next, we'll need to make our bot, and add it to our server. Get started by visiting the (Discord Developer Portal)[https://discord.com/developers/applications], hitting "New Application", giving it a suitable name, and agreeing to their policies.

Once you do that, go to "Bot", where you can optionally give it an icon and username (we're leaving that as-is), and we're going to enable *all* of the intents under "Privilged Gateway Intents". This'll allow the bot to see information like message content, presence, and members, without needing to be prompted by a command.

While we're here, we're going to hit "Reset Token", and confirm that we actually want to reset the token. This'll give us a token (`MTMz...`), which we'll need shortly. This can only be viewed once, else you will have to reset it!

Then, we'll go to "Installation", and add the `bot` scope under "Guild Install" (make sure to keep `applications.commands`!). Enable the "Administrator" permission, and save your changes.

Then, take the Discord Provided Link, open up a new tab, and hit "Add to Server", and select the server you've just created. Once you've finished authorizing the bot, you're done with Discord!

Remember that `.env` file we created? Open that up, and fill in the blanks! Specifically, replace `DISCORD_TOKEN` with the token you regenerated (`MTMz...`), and `TEST_GUILD_ID` with the server ID you copied earlier.

> [!CAUTION]
> Never share your token with anyone, as it will give them *full* control over your bot. For this reason, the `.env` file should *never* be committed to git!

Right then, we're good to go!

## Running the Bot

To run the bot, simply run the following command:

```sh
$ poetry run python -m c4_discord_bot
```

This will, assuming everything works correctly, load the `.env` file, and connect your bot to Discord, registering the commands to your testing server immediately. You can check by going to your Discord and ensuring that the bot is online.

You can stop the bot at anytime by hitting `Ctrl+C`.

## Adding a Cog (and a Command)

We'll be writing a (really) simple "ping" command that will reply "pong" whenever we run the command.

First, we need to make a new "cog", which is essentially a sub-program that the bot runs. All of these live in `c4_discord_bot/cogs`.

To create a new cog, either copy any existing cog in that folder (renaming the file), or, if you're feeling adventurous, start a new file!

We'll be starting a new file, because there's no simple cogs available at the time of writing.

```py
from discord.ext.commands import Cog, Bot
from discord import Interaction, app_commands

class Ping(Cog):
	def __init__(self, bot: Bot):
		self.bot = bot
	
	@app_commands.command()
	async def ping(self, interaction: Interaction):
		"""Sends a pong when this is ran"""
		await interaction.response.send("Pong!")

async def setup(bot):
	await bot.add_cog(Ping(bot))
```

Starting at the top, we import a class called `Cog`, a class called `Bot`, a class called `Interaction`, and a module for our app commands, and we make our class (called Ping) a subclass of Cog. It's not quite important to know *what* Cog does right now.

Next up, our classic `__init__` method, takes in our bot, and stores a reference to it in our class. Pretty simple!

Next, we have our actual command, identified by the decorator `@app_commands.command()`. This tells the bot that this is a *slash command* with the name `ping` (the name of the function). As we have no other parameters other than `interaction`, which is provided by Discord, it takes no other parameters.

This is followed by a docstring, which the first line will be used for the description in Discord, and our response.

Lastly, outside the class, we have a `setup` function, which takes in our bot and registers the cog to it (by adding `bot.add_cog` with a new instance of the class). This will be run whenever the bot (re-)loads.

Now, since we're creating a new file, we'll also need to go to `client.py` and add the path to `load_cogs`, like so:

```diff
async def load_cogs(self):
	if environ.get("ENV") == "development":
		await self.load_extension("c4_discord_bot.cogs.development")
	await self.load_extension("c4_discord_bot.cogs.neofetch")
+	await self.load_extension("c4_discord_bot.cogs.ping")
```

(The path is the relative path from the main root of our repository, to the file, but replacing all `/` with `.` and removing the `.py` extension, like we're importing it.)

That's it! All we need to do now is test it out!

## Testing Our Command

If you don't have the bot already running, now's a good time to start it. If it's already running, you can keep it running, as we can load our new file and command directly from Discord.

To do this, use the `/load_extension` command, and give it the path we gave to `load_extension(...)` earlier. This'll load our extension into the bot!

(Note: if you're not adding a new extension, you can use `/reload_extension` instead)

Next, we'll need to reload our commands, since we added a new command. We can do this with the `/reload_commands` command!

Give it a second for Discord to recognize our changes, and `/ping` should be active! Try it with `/ping`!

## Adding Arguments

* `str`
* `int`
* `float`
* `bool`
* `discord.User` or `discord.Member`
* `discord.abc.GuildChannel` - channel
* `discord.Role`
* `discord.Attachment`

`app_commands.Range[int, 0, 10]`
`Literal["a", "b", "c"]`

## Not Blocking The Thread

The bot is single-threaded, but it really tries to pretend like it isn't by using copious amounts of async/await. This is usually fine, as the event loop has plenty of chances to catch up with the copious amounts of `await`s everywhere, but it soon becomes a problem when you want to deal with anything CPU-intensive, as it can block the event loop for however long it takes.

To counteract this, there's two methods you can use: either finding async-functions, or by shoving the work onto another thread.

The first way is simple! Instead of using `time.sleep(...)`, use `await asyncio.sleep(...)`! Same job, but one stops the world while the other lets the event loop work on other items while its waiting. There's a couple of other equivalent functions (for subprocesses) within the `asyncio` library, but other libraries do exist on pip for other use-cases (like files with `aiofiles`).

The second way is a little more complicated. You'll need to extract the problematic synchronous code into another function, and calling `await loop.run_in_executor(None, func, *args)`. The future will resolve whenever your synchronous code completes in a background thread, returning the result. (You can see this in action in `cogs/washing_machine.py`.)

## Other Methods

## Common Pitfalls

Here's a list of common pitfalls, or just general sources of trouble:

* If an exception occurs, the bot *will not* notify Discord of the failure, leading to the command either timing out, or it waiting forever. The bot is still active, but it simply doesn't notify Discord something went wrong.
	* There's probably an event you can listen to... but I haven't found the right one yet. Working on it!
* If you frequently relaunch the bot (by hitting `Ctrl+C` and re-running the launch command), the bot may refuse to connect!
* Blocking the thread with CPU intensive tasks! Try not to do this! (Seriously, I've done it way too much, even after writing "Not Blocking The Thread"...)


## Publishing Our Work

Now that you have your beaufiful creation, how *exactly* do we get it on the main bot? Simple, we must submit a **Pull Request**!

To get started, we need to commit our work to the repository that you cloned at the start of this tutorial.

```sh
$ git add c4_discord_bot/cogs/pokemon_generator.py
$ git commit -m "my super cool creation"
$ git push
```

> [!TIP]
> You can use anything you feel comfortable with to commit and push! VS Code has a `Source Control` panel you can use to do the same thing, or you can use something like `lazygit`, `Fork`, or `Github Desktop`.

Once you've done that, you'll need to open up a **Pull Request**. For futher details, see [GitHub's documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)!

Now, all that's left to do is wait. One of us will come and review your awesome command(s), give you feedback if neccessary, and merge your code in! Once that happens, check the bot in a day or so and *presto*!

## Further Reading

I haven't filled in this section on the sign's documentation, so... odds aren't likely this'll be populated anytime soon.
