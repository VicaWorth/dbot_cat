"""
Written by Victoria Worthington

The cat object holds each cat's genetic information, phenotype, and 
cat creation. 

It does NOT contain breeding information.

"""

import pandas as pd
import random 

import mysql.connector

# import numpy as np 
import math
from datetime import datetime
from tabulate import tabulate

import globals
from catimager import CatImager
from savehandler import SaveHandler

# This stops rows and coulmns from being cutoff
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rowwidth', None)

lookupColor = {
            # Sexes
                'M': 'Male',
                'F': 'Female',
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
                'wx': 'None',
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
    def __init__(self, userID, catID, exists : bool):
        # Initializes everything as unknown
        self.userID = userID
        self.catdb = None
        self.sex = 'u'
        self.name = 'Unknown'
        self.id = 0

        self.fatherID = 0
        self.motherID = 0

        self.genes = pd.DataFrame({
                                'LocusO': ['u', 'u'], # Orange
                                'LocusB': ['u', 'u'], # Black/Brown
                                'LocusD': ['u', 'u'], # Dilution
                                'LocusA': ['u', 'u'], # Agouti
                                'LocusS': ['u', 'u'], # Spotting
                                'LocusC': ['u', 'u'] # Colorpoint
                                })
        self.genesPheno = self.genes.copy()
        self.genes.astype('string')

        if exists == True:
            self.id = catID
            self.load_cat()
    
    def seeder():
        random.seed(datetime.now().timestamp())

    def save_name_and_sex(self, name, sex):
        self.name = name
        self.sex = sex
    
    def random_generate_s(self):


            genesHolder = []
            for i in range((len(globals.allChoices))-1):
                r1 = random.randint(0, len(globals.allChoices[i])-1)
                r2 = random.randint(0, len(globals.allChoices[i])-1)
                if r1 < r2:
                    genesHolder.append(globals.allChoices[i][r1])
                    genesHolder.append(globals.allChoices[i][r2])
                else:
                    genesHolder.append(globals.allChoices[i][r2])
                    genesHolder.append(globals.allChoices[i][r1])
            # The create genetics panel will automatically handle
            # male cats and their genetic dependencies (so dont worry about O)
            self.create_genetics(genesHolder)

    # This code is run whenever we do stuff like print(mycat)
    def __str__(self):
        return f"This cat is named {self.name}, sex {self.sex}, with the ID of {self.id}"
    
    def set_parents(self, fatherID, motherID):
        self.fatherID = fatherID
        self.motheriD = motherID

    def get_genes(self):
        return self.genes
    
    def get_phenotype(self):
        return self.genesPheno
    
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
    wx/wx   - No white spotting 

    LocusC = color point gene
    C/-   - No colorpoint
    cb/-  - Burmese
    cb/cs - Tonkinese
    cs/-  - Siamese
    c/c   - Albino
    """

    def create_genetics(self, newGenes):

        # Copies genes given and puts it into self.genes
        self.genes.astype('object')
        for i in range(0,11):
            index = math.ceil((i/2))
            
            if i == 0 and self.sex == "M":
                self.genes.iat[0, index] = newGenes[i]
                self.genes.iat[1, index] = "x"
            else:
                self.genes.iat[0, index] = newGenes[i]
                self.genes.iat[1, index] = newGenes[i+1]
        
        # Creates "phenotype" version of the genes
        # MAKE TOP ROW DOMINANT GENE 
        
        self.genesPheno = self.genes.copy()
        self.genesPheno.astype('object')
        for col in list(self.genesPheno):
            self.genesPheno[col][0] = lookupColor[self.genesPheno[col][0]]
            self.genesPheno[col][1] = lookupColor[self.genesPheno[col][1]]
            # self.genesPheno.at[index, row] = lookupColor[self.genesPheno.at[index, row]]
        
    
    """
    Prints the genetics of a cat in a table,
    the variable alleles (when set to true) will print alleles
    otherwise it will print the gene expression (like orange/black)
    """
    def print_genes(self, allelesTable: bool, phenoTable: bool):
        message = ""
        if (allelesTable):
            message += "Alleles:\n"
            message += tabulate(self.genes, headers='keys', showindex="never") + "\n\n"
            # message += self.genes.to_string() + "\n\n"
            # for index, row in self.genes.iterrows():
                # message += row.to_frame().T + '\n'
            print(message)
        if (phenoTable):
            message += "Alleles' Expression:\n"
            message += tabulate(self.genesPheno, headers='keys', showindex="never")+ "\n\n"
            # message += self.genes.to_string() + "\n\n"
            print(message)
        return message

    """
    Will calculate the cat's phenotype based off of its genes

    Dominant genes always appear first in the pair. This makes it
    easier to calculate which genes should appear and which shouldn't
    For simplicity, Orange always appears before Not Orange.
    """
    def print_phenotype(self):
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
            message = (f"{self.name} is a {lookupColor[self.sex]} {colorpoint} {tabby} (stripes) Tortoiseshell, colored {baseColor[0]} and {baseColor[1]} with {whitespotting} White Spots.")
        else:
            message = (f"{self.name} is a {lookupColor[self.sex]} {colorpoint} {tabby} (stripes) {baseColor[0]} with {whitespotting} White Spots.")
        print(message)
        return message
    
    """
    Prints out main information about cat

    Including: Name, Sex, Id, and an Image of the cat.
    """
    def print_profile(self):
        return f"Template"
    
    def print_image(self):
        image = CatImager()
        return image
    
    def save_cat(self):
        s = SaveHandler()
        s.save_cat(self.userID, self.name, self.sex, self.genes)
    
    def load_cat(self):
        s = SaveHandler()
        self.id, self.name, self.sex, genes = s.load_cat(self.id)
        self.create_genetics(genes)
    
    def load_id(self):
        s = SaveHandler()
        self.id = s.load_id()