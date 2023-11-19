import pandas as pd
import random 
import numpy as np 
import math
from datetime import datetime
random.seed(datetime.now().timestamp())

lookupColor = {
            # Locus O (Orange)
                'O': 'Orange',
                'o': 'Not Orange',
            # Locus B (Brown)
                'B': 'Black',
                'b': 'Chocolate',
                'b1':'Cinnamon',
            # Locus D (Dilution)
                'D': 'Not Diluted',
                'd': 'Diluted',

                'Od': 'Cream',  # diluted orange

                'Bd': 'Blue',   # diluted black
                'bd': 'Lilac',  # diluted chocolate
                'b1d': 'Fawn',  # diluted cinnamon
            # Locus A (Agouti)
                'MC': 'Mackerel', # Cat will have verticle stripes
                'mc': 'Classic',  # Cat will have marbled stripes
                'a': 'Solid',     # The cat will be solid
			# Locus DW (Dominant white which 75% of the time causes deafness)
			#	'DW': 'Dominant White',
            # Locus S (White Spots)
                'Ws': 'Large',
                'ws': 'Small',
            # Locus C (Color point or Siamese)
                'C': 'No Colorpoint',
                'cb': 'Burmese', # cb and cs are incomplete dominance. So together the create a tonkinese
                'cs': 'Siamese',
                'c': 'Albino',
            # No gene
                'x': 'None',
            # Unknown Gene
                'u': 'Unknown'
              }

class Cat:
    def __init__(self, sex, name, randomGen):
        # this right now gets rid of trailling zeros
        # NOTE random generator is not seeded and seeds are apparently
        # depreciated
        self.id = random.randint(1,1_000_000)
        self.sex = sex
        self.name = name

        #                         0        1   2
        self.genes = pd.DataFrame({
                                'LocusO': [0, 1], # Orange
                                'LocusB': [2, 3], # Black/Brown
                                'LocusD': [4, 5], # Dilution
                                'LocusA': [6, 7],
                                'LocusS': [8, 9],
                                'LocusC': [10, 11]
                                })
        # randomGen will create a randomly generated cat.
        # NOTE RIGHT NOW ITS NOT LOOKING AT CAT'S GENDER
        if randomGen == True:
            # This tuple holds the number of options per allele
            # These are the locusts
            #             O B D A S C
            allChoices = (('O','o'),
                          ('B','b','b1'),
                          ('D','d'),
                          ('MC','mc','a'),
                          ('Ws','ws'),
                          ('C','cb','cs','c'))
            genesHolder = []
            for i in range((len(allChoices))):
                r1 = random.randint(0, len(allChoices[i])-1)
                r2 = random.randint(0, len(allChoices[i])-1)
                # print(allChoices[i], allChoices[i][r1], allChoices[i][r2])
                if r1 < r2:
                    genesHolder.append(allChoices[i][r1])
                    genesHolder.append(allChoices[i][r2])
                else:
                    genesHolder.append(allChoices[i][r2])
                    genesHolder.append(allChoices[i][r1])
            self.create_genetics(genesHolder)
                
                    

    # This code is run whenever we do stuff like print(mycat)
    def __str__(self):
        return f"{self.name}"
    
    """
    LocusO = orange gene
    X-Chromosome dependent
    O/O   - Orange
    O/x   - Male Orange

    LocusB = black/brown gene
    B/-   - Black 
    b/b   - Brown
    b1/b1 - Cinnamon

    LocusD = dilution gene
    D/D   - No Dilution
    d/d   - Dilution
    d1/d1 - Double Dilution

    LocusA = stripes/tabby gene
    A/-   - Stripes
    a/a   - No Stripes

    LocusS = white spots gene
    Ws/-  - Large white spots
    ws/-  - Little or no white spots
    x/x   - No white spotting 

    LocusC = color point gene
    C/-   - No colorpoint
    cb/-  - Burmese
    cb/cs - Tonkinese
    cs/-  - Siamese
    c/c   - Albino
    """
    # At some point replace this var input with an array or something :eyeroll:
    def create_genetics(self, newGenes):

        # print(self.genes)
        for i in range(0,11):
            index = math.ceil((i/2))
            
            self.genes.iat[0, index] = newGenes[i]
            self.genes.iat[1, index] = newGenes[i+1]
        
        # Creates "phenotype" version of the genes
        # MAKE TOP ROW DOMINANT GENE 
        
        self.genesPheno = self.genes.copy()
        for col in list(self.genesPheno):
            self.genesPheno[col][0] = lookupColor[self.genesPheno[col][0]]
            self.genesPheno[col][1] = lookupColor[self.genesPheno[col][1]]
            # self.genesPheno.at[index, row] = lookupColor[self.genesPheno.at[index, row]]
    
    """
    Prints the genetics of a cat in a table,
    the variable alleles (when set to true) will print alleles
    otherwise it will print the gene expression (like orange/black)
    """
    def show_genes(self, alleles, nonAlleles):
        if (alleles):
            print("--=-- Genetic (Alleles) --=--")
            print(self.genes, "\n")
        if (nonAlleles):
            print("--=-- Genetic (Non Alleles) --=--")
            print(self.genesPheno,"\n")

    """
    The breeding profile could be used to compare two cats genes
    and their types of offspring.

    It might be useful for it to be able to create Punnett squares.
    These can get extremely large with just a few genes,
    So finding some kind of limitations on that will be important
    """
    def show_breeding_profile(self, mate):
        print("-0-0-0- Breeding Profile -0-0-0- ")

    """
    Will calculate the cat's phenotype based off of its genes

    Dominant genes always appear first in the pair. This makes it
    easier to calculate which genes should appear and which shouldn't
    For simplicity, Orange always appears before Not Orange.
    """
    def phenotype(self):
        message = "Something went wrong."
        O1 = self.genes.iat[0, 0]
        O2 = self.genes.iat[1, 0]
        B1 = self.genes.iat[0, 1]
        # B2 = self.genes.iat[1, 1]
        D1 = self.genes.iat[0, 2]
        D2 = self.genes.iat[1, 2]
        A1 = self.genes.iat[0, 3]
        # A2 = self.genes.iat[1, 3]
        S1 = self.genes.iat[0, 4]
        # S2 = self.genes.iat[1, 4]
        C1 = self.genes.iat[0, 5]
        C2 = self.genes.iat[1, 5]

        baseColor = [lookupColor[O1], '']
        tortie = False
        # Tabby & Whiteness 
        tabby = lookupColor[A1]
        whitespotting = lookupColor[S1]
       
        # Colorpoint calculations
        colorpoint = lookupColor[C1]
        if C1 == 'cb' and C2 == 'cw':
            colorpoint = 'Tonkinese'

        # Checks if black exists
        if O1 != 'O':
            baseColor[0] = lookupColor[B1]
            
        if O1 != 'O' and D1 == 'd' and D2 == 'd':
            baseColor[0] = lookupColor[B1+'d']
        elif O1 == 'O' and D1 == 'd' and D2 == 'd':
            baseColor[0] = lookupColor[O1+'d']

        # Used for finding Torties
        if self.sex == 'F':
            # at [row, column]
            if O1 != O2:
                tortie = True

            if tortie == True:
                if D1 == D2:
                    baseColor[1] = lookupColor[B1+'d']
                elif D1 != D2:
                    baseColor[1] = lookupColor[B1]

        elif self.sex != 'M':
            message = ("Cat's sex cannot be determined.")
        
        if tortie == True:
            message = (f"Your cat is a {colorpoint} {tabby} (stripes) Tortoiseshell, colored {baseColor[0]} and {baseColor[1]} with {whitespotting} White Spots.")
        else:
            message = (f"Your cat is a {colorpoint} {tabby} (stripes) {baseColor[0]} with {whitespotting} White Spots.")
        print(message)
        return message

# mycat = Cat('F', 'Snuggles', True)
"""
LocusO - Orange or Black
LocusB - Chocolate/Cinnamon
LocusD - Dilution or Not
LocusA - Stripes/Tabby gene
LocusS - White Spots gene
LocusC - color point gene
"""
# myGenes = ['O', 'O',
#         'b1','b1',
#         'd','d',
#         'MC','mc',
#         'Ws','x',
#         'C','C']
# mycat.create_genetics(myGenes)
# mycat.show_genes(True, True)
# mycat.phenotype()

