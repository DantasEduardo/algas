import random


class BPM180:
    def __init__(self):
        """Simulate the BPM180 sensor, generating pressure and temperature values"""
        self.pressure = [1003.3, 1013.3, 1030.3]
        self.temperature = [15.8, 17.8, 20.8]

    def __generate_pressure_mean(self) -> float:
        """Generates pressure mean in São Paulo in the period of rain or not"""
        return self.pressure[random.randint(0,2)]


    def __generate_temperature_mean(self) -> float:
        """Generates temperature mean in São Paulo in the period of rain or not"""
        return self.temperature[random.randint(0,2)]


    def simulate_pressure(self):
        """Simulates the pressure in São Paulo"""
        pressure_mean = self.__generate_pressure_mean()
        return round(random.uniform(pressure_mean - 5, pressure_mean + 5), 2)
    
    def simulate_temperature(self):
        """Simulates the temperature in São Paulo"""
        temperature_mean = self.__generate_temperature_mean()
        return round(random.uniform(temperature_mean - 5, temperature_mean + 5), 2)

