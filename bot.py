import discord
from discord import app_commands
from discord.ext import commands
import logging

from cat import Cat
from plotter import Plotter
from breeding import Breeding 
from savehandler import SaveHandler
            
logging.basicConfig(level=logging.INFO)

TESTING_GUILD_ID = 913140922085171240  # Replace with your guild ID

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def helpCat(ctx):
    message = "# Catbot! WOOHOO\n Commands are run via >\n"
    message += "## >generateNewRandomCat name sex\n Will generate a new cat"
    message += "\n## >loadCat id\n Will load a new cat"
    message += "\n## >breedCats motherID fatherID\n Will breed two cats"
    await ctx.send(content=message)

@bot.command()
async def generateNewRandomCat(ctx, name="Snuggles", sex="u"):
    if name.isalpha() and sex == "M" or "F":
        userID = ctx.author.id

        newCat = Cat(userID, 0, False)
        newCat.new_cat_creation(sex, name)

        message0, message1 = plot_one_cat(newCat, name)
        
        table = discord.File(f"tables/{name}.png")
        await ctx.send(file=table, content=f"{message0}\n{message1}")
    else:
        await ctx.reply("You inputed something incorrectly.")

@bot.command()
async def generateNewCatWithGenes(ctx, name, sex, o1,o2,b1,b2,d1,d2,a1,a2,s1,s2,c1,c2):
    if name.isalpha() and sex == "M" or "F":
        userID = ctx.author.id
        genes = [o1,o2,b1,b2,d1,d2,a1,a2,s1,s2,c1,c2]
        newCat = Cat(userID, 0, False)
        newCat.new_cat_creation(sex, name, False, genes)

        message0, message1 = plot_one_cat(newCat, name)

        table = discord.File(f"tables/{name}.png")
        await ctx.send(file=table, content=f"{message0}\n{message1}")
    else:
        await ctx.reply("You inputed something incorrectly.")

@bot.command()
async def loadCat(ctx, catID):
    userID = ctx.author.id

    newCat = Cat(userID, catID, True)
    message0 = newCat
    message1 = newCat.print_phenotype()

    id = newCat.load_id()

    tablesToPrint = []
    new_genes1 = newCat.get_genes()
    new_genes2 = newCat.get_phenotype()
    tablesToPrint.append(new_genes1)
    tablesToPrint.append(new_genes2)
    chartNames = [f"{newCat.name}'s Alleles", f"{newCat.name}'s Phenotype"]
    plotted = Plotter(tablesToPrint, chartNames, "newtable")

    table = discord.File(f"tables/newTable.png")
    await ctx.send(file=table, content=f"{message0}\n{message1}")

@bot.command()
async def breedCats(ctx, motherID, fatherID, childName):
    userID = ctx.author.id

    mom = Cat(userID, motherID, True)
    dad = Cat(userID, fatherID, True)
    
    pair = Breeding(userID, mom, dad)
    child = pair.get_child()
    child.name = childName
    child.load_id()
    child.save_cat()
    saveHandler = SaveHandler()
    saveHandler.save_lineage(mom.id, dad.id, child.id)
    message0 = child.print_phenotype()
    
    tablesToPrint = [ ]
    mg1 = mom.get_genes()
    fg1 = dad.get_genes()
    nc1 = child.get_genes()

    tablesToPrint.append(mg1)
    tablesToPrint.append(fg1)
    tablesToPrint.append(nc1)

    chartNames = [f"{mom.name}'s Alleles", f"{dad.name}'s Alleles", "Child's Alleles"]
    plotted = Plotter(tablesToPrint, chartNames, 'unnamed')

    table = discord.File(f"tables/unnamed.png")
    await ctx.send(file=table, content=f"random bred pair\n{message0}")

# https://github.com/openai/shap-e/tree/main
# https://huggingface.co/spaces/hysts/Shap-E

def plot_one_cat(newCat, name):
    message0 = newCat
    message1 = newCat.print_phenotype()

    tablesToPrint = []
    new_genes1 = newCat.get_genes()
    new_genes2 = newCat.get_phenotype()
    tablesToPrint.append(new_genes1)
    tablesToPrint.append(new_genes2)
    chartNames = [f"{name}'s Alleles", f"{name}'s Phenotype"]
    Plotter(tablesToPrint, chartNames, name)

    return message0, message1

bot.run('MTE1MzE0Nzg4MzAxMzU1ODM1Mg.GYFXfO.3FpcxkehsWuI27hyEJZMmTJk6Bd_7i36f1Kods')