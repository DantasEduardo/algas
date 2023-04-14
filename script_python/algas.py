import argparse
import psutil
import random
import time
from datetime import date
from sys import getsizeof 
from src.sensores.anemometro import Anemometro
from src.sensores.bmp180 import BPM180
from src.utils.save_data import SaveData


QUERY_INFOS = f"INSERT INTO infos(time_taken, bytes_used, cpu_used, ram_used, ingestion_date) VALUES (%s,%s,%s,%s,%s)"
QUERY_MEDIDAS = f"INSERT INTO medidas(sensor, value, ingestion_date) VALUES (%s,%s,%s)"


def time_execution(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f'INFO: Executed in {end - start} seconds.\n\n')
        return result
    return wrapper

def transaction_test(block, bd):
    print("Started transaction testing...")
    data = date.today()
    for value in block: 
        start_time = time.time() 
        bytes_int = 0 
        for i in range(value): 
            air_speed = round(random.uniform(0, 120),2) 
            atmospheric_pressure = round(random.uniform(1000, 1020),2) 
            bytes_int = bytes_int + getsizeof(air_speed) + getsizeof(atmospheric_pressure)
            time.sleep(0.01)
            end_time = time.time()
        
        execution_time = end_time - start_time
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        bd.insert(QUERY_INFOS, [execution_time, bytes_int, cpu, ram, data])
        bd.insert(QUERY_MEDIDAS, ["BMP180", atmospheric_pressure, data])
        bd.insert(QUERY_MEDIDAS, ["anemometro", air_speed, data])

    print(f"{value} concluded")

def run(bd):
    bpm = BPM180()
    anemometro = Anemometro()

    temperature_mean = bpm.generate_temperature_mean()
    pressure_mean = bpm.generate_pressure_mean()
    air_speed_mean = anemometro.generate_speed_air_mean()

    count = 60
    while True:
        data = date.today()
        if count < 60:
            temperature_mean = bpm.generate_temperature_mean()
            pressure_mean = bpm.generate_pressure_mean()
            air_speed_mean = anemometro.generate_speed_air_mean()
            count -= 1
        
        temperature = bpm.simulate_temperature(temperature_mean)
        pressure = bpm.simulate_pressure(pressure_mean)
        air_speed = anemometro.simulate_speed_air(air_speed_mean)

        bd.insert(QUERY_MEDIDAS, ["BMP180", pressure, data])
        bd.insert(QUERY_MEDIDAS, ["BMP180", temperature, data])
        bd.insert(QUERY_MEDIDAS, ["anemometro", air_speed, data])

        count -= 1


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
            transaction_test(block, mybd)

    elif params.run:
        run(mybd)
        
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
