import random

class DHT11():
    def __init__(self) -> None:
        """Simulate the DHT11 sensor, generating humidity values"""
        self.batery = 100.0
        self.humidity = (40,60)

    def get_batery(self)->float: return self.batery 
        
    def simulate_humidity(self):
        self.batery -= 0.2
        return random.uniform(*self.humidity)
    
