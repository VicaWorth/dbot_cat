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
# import math
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
        
        if self.breedable:
            self.punnetts = self.generate_punnetts()
            # print(self.punnetts)
            self.create_random_loadout()

    def create_random_loadout(self):
        genesTemplate = ['u', 'u',
                        'u','u',
                        'u','u',
                        'u','u',
                        'u','u',
                        'u','u']
        for i in range(len(self.punnetts)):
            punnett = self.punnetts[i]
            print(punnett.get('Chance'))
            # print(random.choices(self.punnetts[i], weights=self.punnetts[i].get('Chance')))
        

    def __str__(self):
        if self.breedable:
            return f"{self.mother} and {self.father} are a viable pair."
        else:
            return f"The cats provided cannot be bred. Check that you've provided a male and female cat."

    """
    Should be run AFTER generating punnetts.
    """
    def print_punnet(self, locus):
        return "Eventually returns punnett square specified"

    def generate_punnetts(self):
        if self.breedable == False:
            return "Not breedable"
        # columnHeaders = ['LocusO','LocusB', 'LocusD','LocusA','LocusS', 'LocusC']
        punnetts = []
        # punnetts.astype('object')

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
        locuses = ['LocusO','LocusB','LocusD','LocusA','LocusS','LocusC']
        for i in range((len(allChoices))-1):
                punnett = self.generate_punnett(lookupGene, locuses[i], i)
                punnetts.append(punnett)
                # print(punnett)

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
        
        # print(punnett)
        # print(punnett.value_counts("MA1"), punnett.value_counts("MA2"))
        punnett.columns = ['MA1', 'MA2']
        percentages = punnett.value_counts('MA1').add(punnett.value_counts('MA2'), fill_value=0)
        percentages *= 25
        # print(percentages)
        newDf = percentages.to_frame(name=locus).reset_index()
        newDf.rename(columns={0:'Alleles', 1:'Chance'})
        return newDf

mother = Cat('F', 'Snuggles', True)
father = Cat('M', 'Fluffy', True)

pair = Breeding(mother, father)
#pair.generate_punnetts(False)

