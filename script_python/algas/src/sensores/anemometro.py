import random


class Anemometro:
    def __init__(self):
        """Simulate a Anemometro, generating speed of air metrics"""
        self.speed_mean = [9.6, 15.6, 19.6]
        self.batery = 100.0

    def get_batery(self): return self.batery 

    def generate_speed_air_mean(self) -> float:
        """Generates speed air mean in São Paulo in the period of rain or not"""
        return self.speed_mean[random.randint(0,2)]

    def simulate_speed_air(self, speed_air_mean:float) -> float:
        """Simulates the speed air in São Paulo"""
        self.batery -= 0.5
        return round(random.uniform(speed_air_mean - 5, speed_air_mean + 5), 2)

