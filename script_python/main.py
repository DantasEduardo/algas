import argparse
import getpass
import time
from src.utils.save_data import SaveData
import src.algas as algas 

def time_execution(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f'INFO: Executed in {end - start} seconds.\n\n')
        return result
    return wrapper

@time_execution
def main(params):
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
        mybd = SaveData()
        for block in blocks:
            algas.transaction_test(block, mybd)

    elif params.run:
        host = str(input("Enter the host: "))
        db = str(input("Enter the database: "))
        user = str(input("Enter the user: "))
        psd = getpass.getpass(prompt="Enter database password:")
        mybd = SaveData(host=host,
                        database=db, 
                        user=user,
                        password=psd)
        algas.run(mybd)
        
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
    args = parser.parse_args()

    main(args)