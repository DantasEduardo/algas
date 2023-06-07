import random

class TCRT5000():
    def __init__(self) -> None:
        """Simulate the TCRT5000 sensor, simulating a capacity and amount of soybeans colected"""
        self.batery = 100.0
        self.silo_capacity = (4800,5000)
        self.soybeans_collected  = (3600,4800)

    def get_batery(self)->float: return self.batery 
        
    def simulate_silo_capacity(self):
        self.batery -= 0.2
        return random.uniform(*self.silo_capacity)
    
    def simulate_soybeans_collected(self):
        self.batery -= 0.2
        return random.uniform(*self.soybeans_collected)
    