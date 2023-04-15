import psutil
import random
import time
from datetime import date
from sys import getsizeof 
from src.sensores.anemometro import Anemometro
from src.sensores.bmp180 import BPM180


QUERY_INFOS = f"INSERT INTO infos(time_taken, bytes_used, cpu_used, ram_used, ingestion_date) VALUES (%s,%s,%s,%s,%s)"
QUERY_MEDIDAS = f"INSERT INTO medidas(sensor, value, ingestion_date) VALUES (%s,%s,%s)"

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
    print("Started simulation")
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

        print("Insert data into bd")
        bd.insert(QUERY_MEDIDAS, ["BMP180", pressure, data])
        bd.insert(QUERY_MEDIDAS, ["BMP180", temperature, data])
        bd.insert(QUERY_MEDIDAS, ["anemometro", air_speed, data])

        count -= 1

