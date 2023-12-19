import discord
from discord import app_commands
from discord.ext import commands
import logging

from cat import Cat
from breeding import Breeding 
            
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
        message1 = newCat.print_phenotype()
        newCat.create_tables()
        
        table = discord.File(f"tables/{name}.png")
        await ctx.send(file=table, content=f"{message0}\n{message1}")
    else:
        await ctx.reply("You inputed something incorrectly.")

@bot.command()
async def breedCats(ctx):
    mom = Cat('F', "Mother", True)
    dad = Cat('M', "Father", True)
    
    pair = Breeding(mom, dad)
    child = pair.get_child()
    message0 = child.print_phenotype()
    
    table = discord.File(f"tables/unnamed.png")
    await ctx.send(file=table, content=f"random bred pair\n{message0}")

bot.run('MTE1MzE0Nzg4MzAxMzU1ODM1Mg.GYFXfO.3FpcxkehsWuI27hyEJZMmTJk6Bd_7i36f1Kods')

# https://github.com/openai/shap-e/tree/main
# https://huggingface.co/spaces/hysts/Shap-E
