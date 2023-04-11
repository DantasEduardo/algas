import argparse
import psutil
import random
import mysql.connector
from matplotlib import pyplot as plt
from time import time, sleep
from datetime import date
from sys import getsizeof 


mydb = mysql.connector.connect(
    host = "localhost",
    user = 'root',
    password = "yh@852147",
    database = "test"
)
mycursor = mydb.cursor()

sql_query = f"INSERT INTO test_1(sensor, time_taken, bytes_used, cpu_used, ram_used) VALUES ('sensor',%s,%s,%s,%s)"
sql_query2 = f"INSERT INTO medidas(sensor, value, ingestion_date) VALUES (%s,%s,%s)"


def transaction(block):
    print("Started transaction testing...")    
    for value in block: 
        start_time = time() 
        bytes_int = 0 
        for i in range(value): 
            air_speed = round(random.uniform(0, 120),2) 
            atmospheric_pressure = round(random.uniform(1000, 1020),2) 
            bytes_int = bytes_int + getsizeof(air_speed) + getsizeof(atmospheric_pressure)
            sleep(0.01)
            end_time = time()
        
        execution_time = end_time - start_time
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        mycursor.execute(sql_query, [execution_time, bytes_int, cpu, ram])
        mycursor.execute(sql_query2, ["BMP180", atmospheric_pressure, date.today()])
        mycursor.execute(sql_query2, ["anemometro", air_speed, date.today()])
        mydb.commit()
    
    print(f"{value} concluded")


def main(params):
    blocks = []
    if params.first:
        print("Setting first test")
        blocks.append([x for x in range(1, 1000, 100)])

    if params.second:
        print("Setting second test")
        blocks.append([x for x in range(1, 1000, 10)])

    if params.third:
        print("Setting third test")
        blocks.append([x for x in range(1, 1000, 1)])

    if params.all:
        print("Setting all tests")
        blocks = [
            block for block in 
            [
                [x for x in range(1, 1000, 100)],
                [x for x in range(1, 1000, 10)],
                [x for x in range(1, 1000, 1)]
            ]
        ]

    if len(blocks) == 0:
        raise Exception('Parameters not set.\nType -h to see all parameters.')    

    for block in blocks:
        transaction(block)


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

    args = parser.parse_args()

    main(args)
