import random


class Anemometro:
    def __init__(self):
        """Simulate a Anemometro, generating speed of air metrics"""
        self.speed_mean = [9.6, 15.6, 19.6]

    def __generate_speed_air_mean(self) -> float:
        """Generates speed air mean in São Paulo in the period of rain or not"""
        return self.speed_mean[random.randint(0,2)]

    def simulate_speed_air(self):
        """Simulates the speed air in São Paulo"""
        speed_air_mean = self.__generate_speed_air_mean()
        return round(random.uniform(speed_air_mean - 5, speed_air_mean + 5), 2)

