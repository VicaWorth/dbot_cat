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
    # Mother & father are the different parents of the cat.
    # NOTE Nothing atm is checking the genders of the parent cats 
    def __init__(self, mother, father):
        self.mother = mother
        self.father = father

    def __str__(self):
        return f"Template"
    
    def generate_punnett(sex):
        punnett = pd.DataFrame({'LocusO': [0,1]})

        # This is being copy pasted from cat.py
        allChoices = (('O','o'),
                        ('B','b','b1'),
                        ('D','d'),
                        ('MC','mc','a'),
                        ('Ws','ws'),
                        ('C','cb','cs','c'),
                        ('x'))
        genesHolder = []
        for i in range((len(allChoices))-1):
            r1 = random.randint(0, len(allChoices[i])-1)
            r2 = random.randint(0, len(allChoices[i])-1)
            if r1 < r2:
                genesHolder.append(allChoices[i][r1])
                genesHolder.append(allChoices[i][r2])
            else:
                genesHolder.append(allChoices[i][r2])
                genesHolder.append(allChoices[i][r1])
        if sex == 'M':

            print(punnett)
        elif sex == 'F':

            print(punnett)
        return punnett