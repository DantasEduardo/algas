import psutil
import random
import time
from datetime import date
from sys import getsizeof 
from src.sensores.anemometro import Anemometro
from src.sensores.bmp180 import BPM180


QUERY_INFOS = f"INSERT INTO infos(time_taken, bytes_used, cpu_used, ram_used, ingestion_date) VALUES (%s,%s,%s,%s,%s)"
QUERY_MEDIDAS = f"INSERT INTO medidas(sensor, value, ingestion_date) VALUES (%s,%s,%s)"

def transaction_test(block:list, bd:object, s3:object) -> None:
    """
    Test a number of transactions in a local machine or in cloud and get performance metrics
    
    Args:
        block (list): a list of numbers
        bd (DBConnector): a class to comunicate with the database   
        s3 (S3Connection): a class to connect to the AWS S3 bucket
    """

    print("Started transaction testing...")
    data = date.today()
    for value in block: 
        start_time = time.time() 
        to_s3_info = {'time_taken':[],
                      'bytes_used':[],
                      'cpu_used':[],
                      'ram_used':[],
                      'ingestion_date':[]}
        
        to_s3_medidas = {'sensor':[],                      
                         'value':[],                    
                         'ingestion_date':[]}

        bytes_int = 0 
        for i in range(value): 
            #fake colect metrics
            air_speed = round(random.uniform(0, 120),2) 
            atmospheric_pressure = round(random.uniform(1000, 1020),2) 
            bytes_int = bytes_int + getsizeof(air_speed) + getsizeof(atmospheric_pressure)
            time.sleep(0.01)
            end_time = time.time()
        
        execution_time = end_time - start_time
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        bd.insert(QUERY_INFOS, [execution_time, bytes_int, cpu, ram, data])
        bd.insert(QUERY_MEDIDAS, ["block_test", atmospheric_pressure, data])
        bd.insert(QUERY_MEDIDAS, ["block_test", air_speed, data])

        if s3:
            to_s3_info['time_taken'].append(execution_time)
            to_s3_info['bytes_used'].append(bytes_int) 
            to_s3_info['cpu_used'].append(cpu) 
            to_s3_info['ram_used'].append(ram) 
            to_s3_info['ingestion_date'].append(data)
            
            to_s3_medidas['sensor'].append("BMP180") 
            to_s3_medidas['value'].append(atmospheric_pressure)
            to_s3_medidas['ingestion_date'].append(data)
            to_s3_medidas['sensor'].append("anemometro")
            to_s3_medidas['value'].append( air_speed)
            to_s3_medidas['ingestion_date'].append(data)

    if s3:
        s3.s3_upload(to_s3_info, 'info')    
        s3.s3_upload(to_s3_medidas, 'medidas') 
        
    print(f"{value} concluded")

def run(bd:object, s3:object=None, iot:object=None) -> None:
    """
    Simulate the operation of BMP180 and a Anemometro
    
    Args:
        bd (DBConnector): a class to comunicate with the database   
        s3 (S3Connection): a class to connect to the AWS S3 bucket
        iot (IoTHub): a class to connect to the Azure IoT Hub
    """
    print("Started simulation")
    to_s3_medidas = {'sensor':[],                      
                    'value':[],                    
                    'ingestion_date':[]}
    bpm = BPM180()
    anemometro = Anemometro()

    temperature_mean = bpm.generate_temperature_mean()
    pressure_mean = bpm.generate_pressure_mean()
    air_speed_mean = anemometro.generate_speed_air_mean()

    count = 60
    while bpm.get_batery() > 0 and anemometro.get_batery() > 0:
        data = date.today()
        if count < 60:
            #after 60 times change the mean randomly
            temperature_mean = bpm.generate_temperature_mean()
            pressure_mean = bpm.generate_pressure_mean()
            air_speed_mean = anemometro.generate_speed_air_mean()
            count = 60
        
        temperature = bpm.simulate_temperature(temperature_mean)
        pressure = bpm.simulate_pressure(pressure_mean)
        air_speed = anemometro.simulate_speed_air(air_speed_mean)

        if random.randint(0,10)>3:
            print("Insert data into bd")
            bd.insert(QUERY_MEDIDAS, ["BMP180", pressure, data])
            bd.insert(QUERY_MEDIDAS, ["BMP180", temperature, data])
            bd.insert(QUERY_MEDIDAS, ["anemometro", air_speed, data])

            if s3:
                to_s3_medidas['sensor'].append("BMP180") 
                to_s3_medidas['value'].append(pressure)
                to_s3_medidas['ingestion_date'].append(data)
                to_s3_medidas['sensor'].append("BMP180") 
                to_s3_medidas['value'].append(temperature)
                to_s3_medidas['ingestion_date'].append(data)
                to_s3_medidas['sensor'].append("anemometro")
                to_s3_medidas['value'].append( air_speed)
                to_s3_medidas['ingestion_date'].append(data)

            if iot:
                print("Insert data into IoT Hub")
                iot.send_message([temperature, pressure, air_speed, 
                                  bpm.get_batery(), anemometro.get_batery()])
        else:
            print("Error getting data")

        count -= 1
    