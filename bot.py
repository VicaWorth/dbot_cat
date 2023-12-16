import discord
from discord import app_commands
from discord.ext import commands
import logging

from cat import Cat
# import tabulate
            
logging.basicConfig(level=logging.INFO)

TESTING_GUILD_ID = 913140922085171240  # Replace with your guild ID

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def generateCat(ctx, name="Snuggles", gender="u"):
    if name.isalpha() and gender == "M" or "F":
        newCat = Cat(gender, name, True)
        message0 = newCat 
        message1 = newCat.print_phenotype()+ '\n'
        message2 = newCat.print_genes(True, True)
        print(message1, message2)
        await ctx.reply(f"{message0}\n{message1}\n```{message2}```")
    else:
        await ctx.reply("You inputed something incorrectly.")

bot.run('MTE1MzE0Nzg4MzAxMzU1ODM1Mg.GYFXfO.3FpcxkehsWuI27hyEJZMmTJk6Bd_7i36f1Kods')

# https://github.com/openai/shap-e/tree/main
# https://huggingface.co/spaces/hysts/Shap-E
