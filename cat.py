import pandas as pd
import random 
import numpy as np 

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

                'Od': 'Cream', # diluted orange

                'Bd': 'Blue',  # diluted black
                'bd': 'Lilac', # diluted chocolate
                'b1d': 'Fawn',  # diluted cinnamon
            # Locus A (Agouti)
                'A': 'Tabby', # Cat will have stripes
                'a': 'Solid', # The cat will be solid
			# Locus DW (Dominant white which 75% of the time causes deafness)
			#	'DW': 'Dominant White',
            # Locus S (White Spots)
                'N': 'Normal (no white)',
                'WS': 'White spotting',
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
    def __init__(self, sex, name):
        # this right now gets rid of trailling zeros
        self.id = random.randint(1,1_000_000)
        self.sex = sex
        self.name = name

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
    def create_genetics(self, o1, o2, 
                        b1, b2, 
                        d1, d2,
                        a1, a2,
                        s1, s2,
                        c1, c2
                        ):
        #                         0        1   2
        self.genes = pd.DataFrame({
                                'LocusO': [o1, o2], # Orange
                                'LocusB': [b1, b2], # Black/Brown
                                'LocusD': [d1, d2], # Dilution
                                'LocusA': [a1, a2],
                                'LocusS': [s1, s2],
                                'LocusC': [c1, c2]
                                })
        
        # Creates "phenotype" version of the genes
        # MAKE TOP ROW DOMINANT GENE 
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
        # B2 = self.genes.iat[1, 1]
        D1 = self.genes.iat[0, 2]
        D2 = self.genes.iat[1, 2]
        A1 = self.genes.iat[0, 3]
        A2 = self.genes.iat[1, 3]
        S1 = self.genes.iat[0, 4]
        S2 = self.genes.iat[1, 4]
        C1 = self.genes.iat[0, 5]
        C2 = self.genes.iat[1, 5]

        baseColor = [lookupColor[O1], '']
        tortie = False

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
LocusA - Stripes/Tabby gene
LocusS - White Spots gene
LocusC - color point gene
"""
mycat.create_genetics('O', 'o',
                      'b1','b1',
                      'd','d',
                      'A','a',
                      'Ws','x',
                      'C','C'
                      )
mycat.show_genes(True, True)
mycat.phenotype()