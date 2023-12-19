"""
Written by Victoria Worthington

The breeding object holds information about breeding chances and possibilites.

This object DOES NOT generate the cat. 

"""

# I would like to figure out how to get rid of these imports
# since im just reimporting the same thing from Cat again
# C++ doesnt make you reimport it but I guess it might be
# im not really importing the whole file???
import pandas as pd
import random 
import numpy as np 
# import math
from datetime import datetime
from tabulate import tabulate
random.seed(datetime.now().timestamp())

from cat import Cat

class Breeding:
    def __init__(self, catOne: Cat, catTwo: Cat):
        self.breedable = False
        self.punnetts = None
        if catOne.sex == 'F' and catTwo.sex == 'M':
            self.breedable = True
            self.mother = catOne
            self.father = catTwo
        elif catOne.sex == 'M' and catTwo.sex == 'F':
            self.breedable = True
            self.mother = catTwo
            self.father = catOne
        
        if self.breedable:
            self.punnetts = self.generate_punnetts()

            child = self.create_random_loadout()
            child.print_phenotype()

    """
    This function will generate a potential offspring using the random chances
    from the punnett.
    """
    def create_random_loadout(self):
        if self.punnetts == None:
            self.generate_punnetts()
        else:
            genesTemplate = []
            # NOTE update this to enumerate later
            for i in range(len(self.punnetts)):
                    punnett = self.punnetts[i]

                    columnNameI = punnett.columns[0]
                    columnNameL = punnett.columns[1]

                    # Gets population and weights, converting them from dataframe to series
                    pop = punnett.get(columnNameI).squeeze()
                    weights = punnett.get(columnNameL).squeeze()
                    # print(f"Weights: {weights}\n Type: {type(weights)}")
                    
                    # Checks if the weights are an integer
                    # If they are, it means there is only one weight (100%)
                    if isinstance(weights, np.integer):
                        parsedAlleles = pop.split(',,')
                        print(parsedAlleles)
                        genesTemplate.append(parsedAlleles[0])
                        genesTemplate.append(parsedAlleles[1]) 
                    # Checks if the value given is just X and not X,,x
                    elif ',,' not in pop[0]:
                        genesTemplate.append(pop[0])
                        genesTemplate.append(pop[0])
                    else:
                        unparsedAlleles = random.choices(pop, weights=weights, k=1)
                        # NOTE update this later to be cleaner
                        # Checks same thing as above but after randomly selecting. 
                        if ',,' not in unparsedAlleles[0]:
                            genesTemplate.append(unparsedAlleles[0])
                            genesTemplate.append(unparsedAlleles[0])
                        else:
                            parsedAlleles = unparsedAlleles[0].split(',,')     
                            genesTemplate.append(parsedAlleles[0]) 
                            genesTemplate.append(parsedAlleles[1])

            # print(genesTemplate)
            child = Cat('u', 'unnamed', False)
            child.create_genetics(genesTemplate)
            print("Child")
            child.print_genes(True, False)
            return child
        

    def __str__(self):
        if self.breedable:
            return f"{self.mother} and {self.father} are a viable pair."
        else:
            return f"The cats provided cannot be bred. Check that you've provided a male and female cat."

    """
    Should be run AFTER generating punnetts.
    """
    def print_punnet(self, locus):
        for punnett in self.punnetts:
            if punnett.columns[1] == locus:
                print(punnett)
                return punnett
        print("Not found")
        return "Punnett for that Locus was not found."

    def generate_punnetts(self):
        if self.breedable == False:
            return "Could not generate punnetts. Check if pair provided can breed."
        punnetts = []
        # punnetts.astype('object')

        # NOTE This has all been copy pasted from cat.py
        allChoices = (  ('O','o'),
                        ('B','b','b1'),
                        ('D','d'),
                        ('MC','mc','a'),
                        ('Ws','ws'),
                        ('C','cb','cs','c'),
                        ('x'))
        lookupGene = ('O','o',
                      'B','b','b1',
                      'D','d',
                      'MC','mc','a',
                      'Ws','ws',
                      'C','cb','cs','c',
                      'x')
        locuses = ['LocusO','LocusB','LocusD','LocusA','LocusS','LocusC']
        for i in range((len(allChoices))-1):
                punnett = self.generate_punnett(lookupGene, locuses[i], i)
                punnetts.append(punnett)

        return punnetts
    
    """
    Helper function of generate_punnetts that does most of the heavy lifting
    """
    def generate_punnett(self, lookupGene, locus, index):
        MA1 = self.mother.genes.iat[0, index]
        MA2 = self.mother.genes.iat[1, index]

        MI1 = lookupGene.index(MA1)
        MI2 = lookupGene.index(MA2)

        FA1 = self.father.genes.iat[0, index]
        FA2 = self.father.genes.iat[1, index]

        FI1 = lookupGene.index(FA1)
        FI2 = lookupGene.index(FA2)

        # Creates a punnett square of the Locus
        columnHeaders = [MA1, MA2]
        body =  (['u', 'u'], 
                 ['u', 'u'])
        punnett = pd.DataFrame(body, columns=columnHeaders)
        punnett.index = [FA1, FA2]

        # NOTE EVENTUALLY CLEAN THIS UP !!

        # Top left square
        if MI1 <= FI1:# r /c
            punnett.iat[0, 0] = MA1 + ',,' + FA1
        elif MI1 > FI1:
            punnett.iat[0, 0] = FA1 + ',,' + MA1

        # Top right square
        if MI2 <= FI1:
            punnett.iat[0, 1] = MA2 + ',,' + FA1
        elif MI2 > FI1:
            punnett.iat[0, 1] = FA1 + ',,' + MA2
        
        if FA2 != 'x':
            # Bottom left square
            if MI1 <= FI2:
                punnett.iat[1, 0] = MA1 + ',,' + FA2
            elif MI1 > FI2:
                punnett.iat[1, 0] = FA2 + ',,' + MA1

            # Bottom right square
            if MI2 <= FI2:
                punnett.iat[1, 1] = MA2 + ',,' + FA2
            elif MI2 > FI2:
                punnett.iat[1, 1] = FA2 + ',,' + MA2
        else:
            punnett.iat[1, 0] = MA1
            punnett.iat[1, 1] = MA2
        
        punnett.columns = ['MA1', 'MA2']
        percentages = punnett.value_counts('MA1').add(punnett.value_counts('MA2'), fill_value=0)
        percentages *= 25

        newDf = percentages.to_frame(name=locus).reset_index()
        newDf.rename(columns={0:'Alleles', 1:'Chance'})
        return newDf

print("\n\nMOTHER")
mother = Cat('F', 'Snuggles', True)
mother.print_genes(True, False)
mother.print_phenotype()

print("\n\nFATHER")
father = Cat('M', 'Fluffy', True)
father.print_genes(True, False)
father.print_phenotype()
print("\n\n")

pair = Breeding(mother, father)
pair.print_punnet("LocusA")

