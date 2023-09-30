import nextcord
import random
from nextcord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

TESTING_GUILD_ID = 913140922085171240  # Replace with your guild ID

bot = commands.Bot()

@bot.slash_command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.slash_command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split("d"))
    except ValueError:
        await ctx.send("Format has to be in NdN!")
        return

    result = ", ".join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(result)


@bot.slash_command(description="For when you wanna settle the score some other way")
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.slash_command()
async def repeat(ctx, times: int, content="repeating..."):
    """Repeats a message multiple times."""
    for _ in range(times):
        await ctx.send(content)


@bot.slash_command()
async def joined(ctx, member: nextcord.Member):
    """Says when a member joined."""
    await ctx.send(f"{member.name} joined in {member.joined_at}")


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subslash_command is being invoked.
    """
    if ctx.invoked_subslash_command is None:
        await ctx.send(f"No, {ctx.subslash_command_passed} is not cool")


bot.run('MTE1MzE0Nzg4MzAxMzU1ODM1Mg.GYFXfO.3FpcxkehsWuI27hyEJZMmTJk6Bd_7i36f1Kods')
# https://github.com/openai/shap-e/tree/main
# https://huggingface.co/spaces/hysts/Shap-E