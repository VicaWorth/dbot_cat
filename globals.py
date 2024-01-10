"""

Global variables declaration

"""

IMAGE_TYPE = 'jpeg'
# This tuple holds the number of options per allele
# These are the locusts
#             O B D A S C
locuses = ['LocusO','LocusB','LocusD','LocusA','LocusS','LocusC']
allChoices = (('O','o'),
                ('B','b','b1'),
                ('D','d'),
                ('MC','mc','a'),
                ('Ws','ws', 'wx'),
                ('C','cb','cs','c'),
                ('x'))

uf = open("../username.txt", "r")
username = uf.read()
uf.close()

pf = open("../password.txt", "r")
password = pf.read()
pf.close()