# What is this?
## This is a Discord bot that can:
- Create and load a genotype and phenotype of a cat.
- Save the cat's genetic information
- Breed two cats and create genetically accurate children

## What doesn't the bot have?
- Error handling
- An easy to use UI
- Long-term usage capabilites (no dedicated server)

## How to read the output?
When the bot responds, it will give an attachment photo of a table with the cat's genes. The dominant genes are the top row, the recessive genes are the bottom row.

# Commands
## /gennewcatrandom [name] [sex]
This command allows you to randomly generate a cat. 
Name must be a string. Sex must be 'F', 'M' or 'u' (for unknown).
![cat4](https://github.com/VicaWorth/dbot_cat/assets/11998960/ad264ea3-19ef-4a8f-855b-d701603c7551)

## /gennewcatinserted [name] [sex] [o1,o2,b1,b2,d1,d2,a1,a2,s1,s2,c1,c2] 
This command allows you to generate a cat with specific values.
Name must be a string. Sex must be 'F', 'M' or 'u' (for unknown).
The other variables are the specific alleles you want the cat to have.
![cat1](https://github.com/VicaWorth/dbot_cat/assets/11998960/c35a7110-6702-47cf-b621-98644a0a27c4)

## /loadcat [catid]
This command allows you to see a cat you've already generated
catid must be an integer. 
![cat3](https://github.com/VicaWorth/dbot_cat/assets/11998960/3b789ec5-df4e-4811-9418-24bf9ad01daa)

## /breedcats [motherid] [fatherid] [childname]
This command will generate an offspring between two cats. 
motherid and fatherid are the parent's ids. 
childname is the name you want to give the new cat. 
![cat2](https://github.com/VicaWorth/dbot_cat/assets/11998960/ff9ad64f-b1a9-4661-be3f-544a6fa0b3b7)


## /showallgenes
This command will show all of the genes and which locus they apart of.
![cat5](https://github.com/VicaWorth/dbot_cat/assets/11998960/5f95dfc9-02ad-43c3-9c71-b49980ebf6c2)


# Project Plan

## Interface with Discord Bot
Step 1:
- [X] Can create a cat via the bot
- [X] Can create pennett square with two cats to see their possible offspring
- [ ] Can check if a certain gene is possible with a pairing
- [ ] Create pictures of cat (We can use emojis/reacts via discord
None of this will be saved, you can just run this while you are using once it shuts off, the data is lost.
Step 2:
- [X]  Save cat data to SQL database

## Cat Genes
Genes
- [X] Add stripes
- [X] Add white spots gene
- [X] Add eye colors (Maybe) <-- polygenes make this impossible unless we wanna do some kind of statistics
- [X] Maybe add color point gene
- [ ] Add fur length gene
- [ ] Add a size gene (if exists)


## Optimization
- [ ] Fix the punnett square generator to be based off of loops rather than manual 
