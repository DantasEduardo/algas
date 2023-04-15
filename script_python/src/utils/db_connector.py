import awswrangler as wr
import pandas as pd
import mysql.connector

class DBConnector:
    def __init__(self, host:str='localhost', user:str='root', password:str=None, database:str=None):
        """Create a connection to the database"""
        try:
            self.mydb = mysql.connector.connect(
                host = host,
                user = user,
                password = password,
                database = database,
                port = "3306"
            )
        except:
            raise Exception("Could not connect to database. Please verify your credentials and host settings") 

        self.mycursor = self.mydb.cursor()


    def insert(self, query:str, values:list) -> None:
        """Insert a register in the database"""
        self.mycursor.execute(query, values)
        self.mydb.commit()


    def close(self) -> None:
        """Close the conection with the database"""
        self.mycursor.close()
        self.mydb.close()
