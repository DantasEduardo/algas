import psutil
import random
import time
from datetime import datetime
from sys import getsizeof 
from src.sensores.anemometro import Anemometro
from src.sensores.bmp180 import BPM180
from src.sensores.npk import NPK
from src.sensores.dht11 import DHT11
from src.sensores.tcrt5000 import TCRT5000

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
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

def run(bd:object=None, s3:object=None, iot:object=None) -> None:
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
    npk = NPK()
    dht = DHT11()
    tcrt = TCRT5000()

    temperature_mean = bpm.generate_temperature_mean()
    pressure_mean = bpm.generate_pressure_mean()
    air_speed_mean = anemometro.generate_speed_air_mean()

    count = 60
    while bpm.get_batery() > 0 and anemometro.get_batery() > 0 and npk.get_batery() > 0\
      and dht.get_batery() > 0 and tcrt.get_batery() > 0:
        
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if count < 1:
            #after 60 times change the mean randomly
            temperature_mean = bpm.generate_temperature_mean()
            pressure_mean = bpm.generate_pressure_mean()
            air_speed_mean = anemometro.generate_speed_air_mean()
            count = 60
        
        temperature = bpm.simulate_temperature(temperature_mean)
        pressure = bpm.simulate_pressure(pressure_mean)
        air_speed = anemometro.simulate_speed_air(air_speed_mean)
        n, p, k = npk.simulate_npk()
        humidity =  dht.simulate_humidity()
        capacity = tcrt.simulate_silo_capacity()
        collected = tcrt.simulate_soybeans_collected()

        if random.randint(0,10)>3:

            if bd:
                print("Insert data into bd")
                bd.insert(QUERY_MEDIDAS, ["BMP180", pressure, data])
                bd.insert(QUERY_MEDIDAS, ["BMP180", temperature, data])
                bd.insert(QUERY_MEDIDAS, ["anemometro", air_speed, data])
                bd.insert(QUERY_MEDIDAS, ["NPK", n, data])
                bd.insert(QUERY_MEDIDAS, ["NPK", p, data])
                bd.insert(QUERY_MEDIDAS, ["NPK", k, data])
                bd.insert(QUERY_MEDIDAS, ["DHT11", humidity, data])
                bd.insert(QUERY_MEDIDAS, ["TCRT5000", capacity, data])
                bd.insert(QUERY_MEDIDAS, ["TCRT5000", collected, data])

            if s3:
                #TODO:
                pass

            if iot:
                print("Insert data into IoT Hub")
                iot.send_message('NPK', [n,p,k,npk.get_batery(),data],'sensor',npk.get_batery()<25)
                iot.send_message('BMP180', [temperature,pressure,bpm.get_batery(),data],'sensor',bpm.get_batery()<25)
                iot.send_message('anemometro', [air_speed,anemometro.get_batery(),data],'sensor',anemometro.get_batery()<25)
                iot.send_message('DHT11', [humidity,dht.get_batery(),data],'sensor',dht.get_batery()<25)
                iot.send_message('TCRT5000', [capacity,collected,tcrt.get_batery(),data],'sensor',tcrt.get_batery()<25)

        else:
            print("Error getting data")
            iot.send_message("Error",["Error getting data"],'sensor',False)

        count-=1
        time.sleep(30)
