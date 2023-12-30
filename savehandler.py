"""
Written by Victoria Worthington

The SaveHandler object deals with SQL connection couldn't have been
done easily inside of the Cat object.

"""

import mysql.connector

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
            user = "readerwriter",
            password = "readerwriter"
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

        self.close_sql()