import mysql.connector

# Creating connection object
# This declaration gives me the heeby jeebies
catdb = mysql.connector.connect(
    host = "localhost",
    user = "readerwriter",
    password = "readerwriter"
)
 
# This object lets us execute SQL in python
cursor = catdb.cursor()

class SaveData:
    def __init__(self, snowflake):
        self.snowflake = snowflake

    def save_cat(self, cat):
        genes = cat.get_genes()
        