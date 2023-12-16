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
# import numpy as np 
import math
from datetime import datetime
from tabulate import tabulate
random.seed(datetime.now().timestamp())

from cat import Cat

class Breeding:
    def __init__(self, catOne: Cat, catTwo: Cat):
        self.breedable = False
        if catOne.sex == 'F' and catTwo.sex == 'M':
            self.breedable = True
            self.mother = catOne
            self.father = catTwo
        elif catOne.sex == 'M' and catTwo.sex == 'F':
            self.breedable = True
            self.mother = catTwo
            self.father = catOne

    def __str__(self):
        if self.breedable:
            return f"{self.mother} and {self.father} are a viable pair."
        else:
            return f"The cats provided cannot be bred. Check that you've provided a male and female cat."
    
    def generate_punnetts(self, sex):
        if self.breedable == False:
            return "Not breedable"
        punnetts = []

        print("MOTHER :")
        self.mother.print_genes(True, False)
        print("Father :")
        self.father.print_genes(True, False)
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
        for i in range((len(allChoices))-1):
                punnett = self.generate_punnett(allChoices, lookupGene, i)
                # Puts that into a list of other punnetts.
                punnetts.append(punnett)
                print(punnett, '\n')

        #print(punnetts)
        # genesHolder = []
        # for i in range((len(allChoices))-1):
        #     r1 = random.randint(0, len(allChoices[i])-1)
        #     r2 = random.randint(0, len(allChoices[i])-1)
        #     if r1 < r2:
        #         genesHolder.append(allChoices[i][r1])
        #         genesHolder.append(allChoices[i][r2])
        #     else:
        #         genesHolder.append(allChoices[i][r2])
        #         genesHolder.append(allChoices[i][r1])
        if sex == 'M':

            print(punnett)
        elif sex == 'F':

            print(punnett)
        return punnetts
    
    """
    Helper function of generate_punnetts that does most of the heavy lifting
    """
    def generate_punnett(self, allChoices, lookupGene, index):
        MA1 = self.mother.genes.iat[0, index]
        MA2 = self.mother.genes.iat[1, index]

        MI1 = lookupGene.index(MA1)
        MI2 = lookupGene.index(MA2)

        FA1 = self.father.genes.iat[0, index]
        FA2 = self.father.genes.iat[1, index]

        FI1 = lookupGene.index(FA1)
        FI2 = lookupGene.index(FA2)

        # print(f"{MA1} {MA2} <- mother genes\n {FA1} {FA2} <- father genes\n ")
        # print(f"{MI1} {MI2} <- mother index\n {FI1} {FI2} <- father index\n ")
        # Creates a punnett square of the Locus
        columnHeaders = [MA1, MA2]
        body =  (['u', 'u'], 
                 ['u', 'u'])
        punnett = pd.DataFrame(body, columns=columnHeaders)
        punnett.index = [FA1, FA2]

        # NOTE EVENTUALLY CLEAN THIS UP !!

        # Top left square
        if MI1 <= FI1:# r /c
            punnett.iat[0, 0] = MA1 + '+' + FA1
        elif MI1 > FI1:
            punnett.iat[0, 0] = FA1 + '+' + MA1

        # Top right square
        if MI2 <= FI1:
            punnett.iat[0, 1] = MA2 + '+' + FA1
        elif MI2 > FI1:
            punnett.iat[0, 1] = FA1 + '+' + MA2
        
        if FA2 != 'x':
            # Bottom left square
            if MI1 <= FI2:
                punnett.iat[1, 0] = MA1 + '+' + FA2
            elif MI1 > FI2:
                punnett.iat[1, 0] = FA2 + '+' + MA1

            # Bottom right square
            if MI2 <= FI2:
                punnett.iat[1, 1] = MA2 + '+' + FA2
            elif MI2 > FI2:
                punnett.iat[1, 1] = FA2 + '+' + MA2
        else:
            punnett.iat[1, 0] = MA1
            punnett.iat[1, 1] = MA2
        
        return punnett

mother = Cat('F', 'Snuggles', True)
father = Cat('M', 'Fluffy', True)

pair = Breeding(mother, father)
pair.generate_punnetts(False)

