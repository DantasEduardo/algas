import awswrangler as wr
import pandas as pd
import mysql.connector

class SaveData:
    def __init__(self, host:str='localhost', user:str='root', password:str=None, database:str=None):
        """Create a connection to the database"""
        self.mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )

        self.mycursor = self.mydb.cursor()


    def insert(self, query:str, values:list) -> None:
        """Insert a register in the database"""
        self.mycursor.execute(query, values)
        self.mydb.commit()


    def close(self) -> None:
        """Close the conection with the database"""
        self.mycursor.close()
        self.mydb.close()
