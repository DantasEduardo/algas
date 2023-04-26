import argparse
import getpass
import pandas as pd
from algas.src.utils.db_connector import DBConnector


def run(db:DBConnector) -> None:
    """
    Run the query in the database and save the results in a parquet file

    Args:
        db (DBConnector): a class to comunicate with the database   

    """

    results = db.select("SELECT * FROM infos;")

    result = {"time_taken": [],
              "bytes_used": [],
              "cpu_used": [],
              "ram_used": []}
    
    for i in results:
        result['time_taken'].append(i[1])
        result['bytes_used'].append(i[2])
        result['cpu_used'].append(i[3])
        result['ram_used'].append(i[4])
    
    df  = pd.DataFrame(data=result)
    print(df.head())
    df.to_parquet(r'.\.\data_algas\data.parquet')


def main(parameters:dict)->None:
    """
    Orchestrator to get and analyze the data from algas
    
    Args:
        parameters (dict): a dictionary of parameters for execution
    """

    if parameters.local:
        db = input("Enter the database: ")
        user = input("Enter the user: ")
        psd = getpass.getpass(prompt="Enter database password:")
        mybd = DBConnector(database=db, 
                           user=user,
                           password=psd)
        run(mybd)

    elif parameters.cloud:
        host = input("Enter the host: ")
        db = input("Enter the database: ")
        user = input("Enter the user: ")
        psd = getpass.getpass(prompt="Enter database password:")
        mybd = DBConnector(host=host,
                           database=db, 
                           user=user,
                           password=psd)
        run(mybd)

    else:
        raise Exception("Parameters not set.\nType -h to see all parameters.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--local', default=False, action='store_true', 
                        help='get results from algas in database local')
    parser.add_argument('-c','--cloud', default=False, action='store_true', 
                        help='get results from algas in database in cloud')
    args = parser.parse_args()
    
    main(args)
