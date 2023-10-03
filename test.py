import pandas as pd
import random 
import numpy as np 

lookupColor = pd.DataFrame([
                            ['O', 'Orange'],
                            ['B', 'Black'],
                            ['b', 'Chocolate'],
                            ['b1', 'Cinnamon']
                           ],
                           columns=['Allele', 'Color from Allele']
                           )

class Cat:
    def __init__(self, sex, name):
        self.id = random.randint(1,1_000_000)
        self.sex = sex
        self.name = name

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
    """
    def create_genetics(self, o1, o2, b1, b2, d1, d2):
        #                                     0        1   2
        self.genes = pd.DataFrame(np.array([['LocusO', o1, o2], 
                                            ['LocusB', b1, b2], 
                                            ['LocusD', d1, d2]]),
                                columns=['Locus','Dominant', 'Recessive'])
    
    def show_genes(self):
        print("Genetic Code")
        print(self.genes)

    """
    Will calculate the cat's phenotype based off of its genes
    """
    def phenotype(self):
        baseColor = 'Unable to Calculate'
        tortie = False

        # Determines what will be expressed
        if self.sex == 'F':
            # at [row, column]
            A1 = self.genes.iat[0, 1]
            print('\n',A1)
            A2 = self.genes.iat[0, 2]
            print(A2)
            if (A1 == A2):
                baseColor = lookupColor.lookup(['O'])
            else:
                baseColor = ["Orange", "Black"]
                tortie = True
        elif self.sex == 'M':
            print("WIP")
        else:
            print("Cat's sex cannot be determined.");
        print(baseColor, tortie)

mycat = Cat('F', 'Snuggles')
mycat.create_genetics('B','B',
                      'b','b1',
                      'D','d')
mycat.show_genes()
mycat.phenotype()