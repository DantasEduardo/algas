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

class S3Connection:
    def __init__(self, bucket:str=None, path:str=None) -> None:
        self.bucket = bucket
        self.path_info = path+'/info/'
        self.path_medidas = path+'/medidas/'
        try:
            wr.s3.does_object_exist(f"s3://{self.bucket}/{path}")
        except:
            raise Exception ("Verify you have access to this bucket or miss type the bucket or path")

    def s3_upload(self, list:dict, type:str) -> None:
        if type=="info":    
            wr.s3.to_parquet(
                df = pd.DataFrame(list),
                bucket=self.bucket,
                path=self.path_info
            )
        elif type=="medidas":
            wr.s3.to_parquet(
                df=pd.DataFrame(list),
                bucket=self.bucket,
                path=self.path_info
            )
        else:
            raise Exception("Invalid type")
