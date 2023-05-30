import argparse
import getpass
import time
import src.algas as algas 
from src.utils.db_connector import DBConnector, S3Connection, IoTHub

def time_execution(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f'INFO: Executed in {end - start} seconds.\n\n')
        return result
    return wrapper

@time_execution
def main(params: dict) -> None:
    """
    Orchestrator to execute the algas test or execute the sensors simulation

    Args:
        params (dict): a dictionary of parameters for execution
    """
    blocks = []
    test = False
    if params.first:
        test = True
        print("Setting first test")
        blocks.append([x for x in range(1, 1000, 100)])

    if params.second:
        test = True
        print("Setting second test")
        blocks.append([x for x in range(1, 1000, 10)])

    if params.third:
        test = True
        print("Setting third test")
        blocks.append([x for x in range(1, 1000, 1)])

    if params.all:
        test = True
        print("Setting all tests")
        blocks = [
            block for block in 
            [
                [x for x in range(1, 1000, 100)],
                [x for x in range(1, 1000, 10)],
                [x for x in range(1, 1000, 1)]
            ]
        ]   

    if test:
        if params.database:
            response = input("Is it a local test?(y/n): ")
            if response.lower() == 'y':
                db = input("Enter the database: ")
                user = input("Enter the user: ")
                psd = getpass.getpass(prompt="Enter database password:")
                mybd = DBConnector(database=db, 
                                    user=user,
                                    password=psd)
                
            elif response.lower() == 'n':
                host = input("Enter the host: ")
                db = input("Enter the database: ")
                user = input("Enter the user: ")
                psd = getpass.getpass(prompt="Enter database password:")
                mybd = DBConnector(host=host,
                                    database=db, 
                                    user=user,
                                    password=psd)
        else:
            mybd = None
        
        if params.upload_s3:
            bucket = input("Enter the bucket: ")
            path = input("In test case we will create a test partition in your path\nEnter the path: ")
            s3 = S3Connection(bucket, path)
        else:
            s3 = None

        for block in blocks:
            algas.transaction_test(block, mybd, s3)

    elif params.run:
        if params.database:
            response = input("Is it a local test?(y/n): ")
            if response.lower() == 'y':
                db = input("Enter the database: ")
                user = input("Enter the user: ")
                psd = getpass.getpass(prompt="Enter database password:")
                mybd = DBConnector(database=db, 
                                    user=user,
                                    password=psd)
                
            elif response.lower() == 'n':
                host = input("Enter the host: ")
                db = input("Enter the database: ")
                user = input("Enter the user: ")
                psd = getpass.getpass(prompt="Enter database password:")
                mybd = DBConnector(host=host,
                                    database=db, 
                                    user=user,
                                    password=psd)
        else:
            mybd = None
        
        if params.upload_s3:
            bucket = input("Enter the bucket: ")
            path = input("In test case we will create a test partition in your path\nEnter the path: ")
            s3 = S3Connection(bucket, path)
        else:
            s3 = None

        if params.azure:
            conection_str = getpass.getpass(prompt="Enter conection string:")
            iot = IoTHub(connection_string=conection_str)
        else:
            iot = None

        algas.run(mybd, s3, iot)
        
    else:
        raise Exception('Parameters not set.\nType -h to see all parameters.')    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--first', default=False, action='store_true', 
                        help='execute the first block of tests')
    parser.add_argument('-s','--second', default=False, action='store_true', 
                        help='execute the second block of tests')
    parser.add_argument('-t','--third', default=False, action='store_true', 
                        help='execute the third block of tests')
    parser.add_argument('-a','--all', default=False, action='store_true', 
                        help='execute the all blocks of tests')
    
    parser.add_argument('-r','--run', default=False, action='store_true', 
                        help='run the sensor simulator')
    
    parser.add_argument('-s3','--upload_s3', default=False, action='store_true', 
                        help='upload the data to a bucket s3')
    
    parser.add_argument('-az','--azure', default=False, action='store_true', 
                        help='upload the data in IoT hub')
    
    parser.add_argument('-db','--database', default=False, action='store_true', 
                        help='insert data in a database')
    
    args = parser.parse_args()

    main(args)
