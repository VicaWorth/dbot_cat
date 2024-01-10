"""
Written by Victoria Worthington

The SaveHandler object deals with SQL connection couldn't have been
done easily inside of the Cat object.

"""

import mysql.connector
import globals

# from cat import Cat

class SaveHandler:
    def __init__(self):
        self.catdb = None

    """
    Creates the SQL connection

    This system might be better if its a global variable
    rather than something that opens and closes all the time
    """
    def setup_sql(self):
        self.catdb = mysql.connector.connect(
            host = "localhost",
            database="discordcatdb",
            user = f"{globals.username}",
            password = f"{globals.password}"
        )

        self.cursor = self.catdb.cursor(buffered=True)

    """
    Clears the SQL connection
    """
    def close_sql(self):
        self.cursor.close()
        self.catdb.close()
        self.catdb = None

    """
        Saves parents of a child
    """
    def save_lineage(self, motherID, fatherID, childID):
        if self.catdb == None:
            self.setup_sql()

        addLineage = ("INSERT INTO lineages"
                 "(fatherid, motherid, childid)"
                 "VALUES (%(fatherid)s, %(motherid)s, %(childid)s)")
        
        dataLineage = {
            'fatherid': fatherID,
            'motherid': motherID,
            'childid': childID
        }

        self.cursor.execute(addLineage, dataLineage)
        self.catdb.commit()    

        self.close_sql()

    def load_cats_by_user(self):
        if self.catdb == None:
            self.setup_sql()
        
        query = (f"SELECT * FROM cats WHERE userid = {self.userID}")

        self.cursor.execute(query)
        self.catdb.commit()

        result = self.cursor.fetchall()
        print(result)

        self.close_sql()

    """
    Saves the current cat into the SQL database
    """
    def save_cat(self, userID, name, sex, genes):
        if self.catdb == None:
            self.setup_sql()
        
        addCat = ("INSERT INTO cats"
                  "(userid, catsname, catssex, LocusO1, LocusO2, LocusB1, LocusB2, LocusD1, LocusD2, LocusA1, LocusA2, LocusS1, LocusS2, LocusC1, LocusC2)"
                  "VALUES (%(userid)s, %(catsname)s, %(catssex)s,  %(LocusO1)s, %(LocusO2)s, %(LocusB1)s, %(LocusB2)s, %(LocusD1)s, %(LocusD2)s, %(LocusA1)s, %(LocusA2)s, %(LocusS1)s, %(LocusS2)s, %(LocusC1)s, %(LocusC2)s)")
        dataCat = {
            # 'catsid': self.id,
            'userid': userID,
            'catsname': name,
            'catssex': sex,
            'LocusO1': genes.iat[0, 0],
            'LocusO2': genes.iat[1, 0],
            'LocusB1': genes.iat[0, 1],
            'LocusB2': genes.iat[1, 1],
            'LocusD1': genes.iat[0, 2],
            'LocusD2': genes.iat[1, 2],
            'LocusA1': genes.iat[0, 3],
            'LocusA2': genes.iat[1, 3],
            'LocusS1': genes.iat[0, 4],
            'LocusS2':  genes.iat[1, 4],
            'LocusC1': genes.iat[0, 5],
            'LocusC2':  genes.iat[1, 5]           
        }

        self.cursor.execute(addCat, dataCat)
        self.catdb.commit()

        self.close_sql()

    """
    Loads a cat into the database
    """
    def load_cat(self, catID):
        if self.catdb == None:
            self.setup_sql()
        
        query = (f"SELECT * FROM cats WHERE catsid = {catID}")
        self.cursor.execute(query)
        self.catdb.commit()

        result = self.cursor.fetchone()

        row = result
        id = row[0]
        name = row[2]
        sex = row[3]
        genes = row[4 : ]

        self.close_sql()
        return id, name, sex, genes
    
    """
    Finds the ID of the latest generated cat  
    """
    def load_id(self):
        if self.catdb == None:
            self.setup_sql()
        
        query = ("SELECT catsid FROM cats ORDER BY catsid DESC LIMIT 1")
        
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        id = result[0]
        
        self.close_sql()
        
        return id

