import random


class BPM180:
    def __init__(self):
        """Simulate the BPM180 sensor, generating pressure and temperature values"""
        self.pressure = [1003.3, 1013.3, 1030.3]
        self.temperature = [15.8, 17.8, 20.8]
        self.batery = 100.0

    def get_batery(self): return self.batery    

    def generate_pressure_mean(self) -> float:
        """Generates pressure mean in São Paulo in the period of rain or not"""
        return self.pressure[random.randint(0,2)]


    def generate_temperature_mean(self) -> float:
        """Generates temperature mean in São Paulo in the period of rain or not"""
        return self.temperature[random.randint(0,2)]


    def simulate_pressure(self, pressure_mean:float) -> float:
        """Simulates the pressure in São Paulo"""
        self.batery -= 0.2
        return round(random.uniform(pressure_mean - 5, pressure_mean + 5), 2)
    
    def simulate_temperature(self, temperature_mean:float) -> float:
        """Simulates the temperature in São Paulo"""
        self.batery -= 0.2
        return round(random.uniform(temperature_mean - 5, temperature_mean + 5), 2)

