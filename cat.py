import pandas as pd
import random 
import numpy as np 


lookupColor = {
            # Locus O
                'O': 'Orange',
                'o': 'Not Orange',
            # Locus B
                'B': 'Black',
                'b': 'Chocolate',
                'b1': 'Cinnamon',
            # Locus D
                'D': 'Not Diluted',
                'd': 'Diluted',
                'Od': 'Cream', # diluted orange
                'Bd': 'Blue',  # diluted black
                'bd': 'Lilac', # diluted chocolate
                'b1d': 'Fawn',  # diluted cinnamon
            # No gene
                'x': 'None',
            # Unknown Gene
                'u': 'Unknown'
              }

class Cat:
    def __init__(self, sex, name):
        self.id = random.randint(1,1_000_000)
        self.sex = sex
        self.name = name

    # This code is run whenever we do stuff like print(mycat)
    def __str__(self):
        return f"{self.name}"
    
    """
    LocusO
    This Locus determines the production of orange/red in the fur.
    The first slot will contain Black for females
    X-Chromosome dependent
    Set o2 to NULL if the at is male

    LocusB
    This locus determins the brown gene. There are three of them:
    B/- -> b/b -> b1/b1

    LocusD the dilution gene
    D/D no dilution
    d/d yes dilution
    d1/d1 yes double dilution
    """
    def create_genetics(self, o1, o2, b1, b2, d1, d2):
        #                         0        1   2
        self.genes = pd.DataFrame({
                                'LocusO': [o1, o2], 
                                'LocusB': [b1, b2], 
                                'LocusD': [d1, d2]
                                })
        
        # Creates "phenotype" version of the genes
        self.genes2 = self.genes.copy()
        for col in list(self.genes2):
            self.genes2[col][0] = lookupColor[self.genes2[col][0]]
            self.genes2[col][1] = lookupColor[self.genes2[col][1]]
            #self.genes2.at[index, row] = lookupColor[self.genes2.at[index, row]]
    
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
            print(self.genes2,"\n")

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
        O1 = self.genes.iat[0, 0]
        O2 = self.genes.iat[1, 0]
        B1 = self.genes.iat[0, 1]
        B2 = self.genes.iat[1, 1]
        D1 = self.genes.iat[0, 2]
        D2 = self.genes.iat[1, 2]

        baseColor = [lookupColor[O1], '']
        tortie = False

        if True:
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
            print("Cat's sex cannot be determined.")
        
        if tortie == True:
            print("Your cat is a tortoiseshell, a", 
                  baseColor[0], "and", baseColor[1],
                  ".")
        else:
            print("Your cat is a", baseColor[0])

mycat = Cat('F', 'Snuggles')
"""
LocusO - Orange or Black
LocusB - Chocolate/Cinnamon
LocusD - Dilution or Not
"""
mycat.create_genetics('o', 'o',
                      'b','b1',
                      'D','d')
mycat.show_genes(True, True)
mycat.phenotype()