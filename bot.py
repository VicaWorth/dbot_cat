import discord
from discord import app_commands
from discord.ext import commands
import logging

import globals
from cat import Cat
from plotter import Plotter
from breeding import Breeding 
from savehandler import SaveHandler
            
logging.basicConfig(level=logging.INFO)

MY_GUILD = discord.Object(id=913140922085171240)

class myBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
intents.message_content = True

bot = myBot(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print('----------------------')

# @bot.tree.tree.command()
# async def helpCat(interaction: discord.Interaction):
#     message = "# Catbot! WOOHOO\n Commands are run via >\n"
#     message += "## >generateNewRandomCat name sex\n Will generate a new cat"
#     message += "\n## >loadCat id\n Will load a new cat"
#     message += "\n## >breedCats motherid fatherid\n Will breed two cats"
#     await interaction.response.send_message(content=message)
    
@bot.tree.command()
async def showallgenes(interaction: discord.Interaction):
    await interaction.response.send_message(content=f"{globals.allChoices}")

@bot.tree.command()
@app_commands.describe(
    name='The name of the cat you are creating',
    sex='The sex of the cat. Enter M,F, or u (case sensitive)',
)
async def gennewcatrandom(interaction: discord.Interaction, name:str, sex:str):
    if name.isalpha() and sex == "M" or sex == "F" or sex == "u":
        userID = interaction.user.id

        newCat = Cat(userID, 0, False)
        newCat.save_name_and_sex(name, sex)
        newCat.random_generate_s()

        newCat.load_id()

        message0, message1, table = plot_one_cat(newCat, newCat.id)
        
        await interaction.response.send_message(file=table, content=f"{message0}\n{message1}")
    else:
        await interaction.response.send_message("You inputed something incorrectly.")

@bot.tree.command()
@app_commands.describe(
    name='The name of the cat you are creating',
    sex='The sex of the cat. Enter M,F, or u (case sensitive)',
    o1='The genes of your cat. To look at valid options, use the showallgenes command'
)
async def gennewcatinserted(interaction: discord.Interaction, name:str, sex: str, o1:str,o2:str,b1:str,b2:str,d1:str,d2:str,a1:str,a2:str,s1:str,s2:str,c1:str,c2:str):
    if name.isalpha() and sex == "M" or "F":
        userID = interaction.user.id
        genes = [o1,o2,b1,b2,d1,d2,a1,a2,s1,s2,c1,c2]
        newCat = Cat(userID, 0, False)
        newCat.save_name_and_sex(name, sex)
        newCat.create_genetics(genes)

        newCat.load_id()

        message0, message1 = plot_one_cat(newCat, newCat.id)

        table = discord.File(f"tables/{newCat.id}.{globals.IMAGE_TYPE}")
        await interaction.response.send_message(file=table, content=f"{message0}\n{message1}")
    else:
        await interaction.response.send_message("You inputed something incorrectly.")

@bot.tree.command()
@app_commands.describe(
    catid='The id of the cat you are trying to look at',
)
async def loadcat(interaction: discord.Interaction, catid:int):
    userID = interaction.user.id

    newCat = Cat(userID, catid, True)
    message0 = newCat
    message1 = newCat.print_phenotype()

    tablesToPrint = []
    new_genes1 = newCat.get_genes()
    new_genes2 = newCat.get_phenotype()
    tablesToPrint.append(new_genes1)
    tablesToPrint.append(new_genes2)
    chartNames = [f"{newCat.name}'s Alleles", f"{newCat.name}'s Phenotype"]
    Plotter(tablesToPrint, chartNames, catid)

    table = discord.File(f"tables/{newCat.id}.{globals.IMAGE_TYPE}")
    await interaction.response.send_message(file=table, content=f"{message0}\n{message1}")

@bot.tree.command()
@app_commands.describe(
    motherid='The ID of the female cat you want to breed',
    fatherid='The ID of the female cat you want to breed',
    childname='The name of the child'
)
async def breedcats(interaction: discord.Interaction, motherid: int, fatherid: int, childname: str):
    userID = interaction.user.id

    mom = Cat(userID, motherid, True)
    dad = Cat(userID, fatherid, True)
    
    message0 = f" Breeding {mom.name} and {dad.name} gives you the child {childname}:"

    pair = Breeding(userID, mom, dad)
    child = pair.get_child()
    child.name = childname
    child.load_id()
    child.save_cat()
    saveHandler = SaveHandler()
    saveHandler.save_lineage(mom.id, dad.id, child.id)
    message1 = child.print_phenotype()
    
    tablesToPrint = [ ]
    mg1 = mom.get_genes()
    fg1 = dad.get_genes()
    nc1 = child.get_genes()

    tablesToPrint.append(mg1)
    tablesToPrint.append(fg1)
    tablesToPrint.append(nc1)

    chartNames = [f"{mom.name}'s Alleles", f"{dad.name}'s Alleles", "Child's Alleles"]
    Plotter(tablesToPrint, chartNames, child.id)

    table = discord.File(f"tables/{child.id}.{globals.IMAGE_TYPE}")
    await interaction.response.send_message(file=table, content=f"f{message0}\n{message1}")

# https://github.com/openai/shap-e/tree/main
# https://huggingface.co/spaces/hysts/Shap-E
    
# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# This context menu command only works on members
@bot.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.response.send_message_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

# Creates the message and image
def plot_one_cat(newCat, imageName: str):
    message0 = newCat
    message1 = newCat.print_phenotype()

    tablesToPrint = []
    new_genes1 = newCat.get_genes()
    new_genes2 = newCat.get_phenotype()
    tablesToPrint.append(new_genes1)
    tablesToPrint.append(new_genes2)
    chartNames = [f"{newCat.name}'s Alleles", f"{newCat.name}'s Phenotype"]
    Plotter(tablesToPrint, chartNames, imageName)

    table = discord.File(f"tables/{newCat.id}.{globals.IMAGE_TYPE}")

    return message0, message1, table

bot.run('MTE1MzE0Nzg4MzAxMzU1ODM1Mg.GYFXfO.3FpcxkehsWuI27hyEJZMmTJk6Bd_7i36f1Kods')