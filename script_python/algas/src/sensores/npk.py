import random

class NPK():
    def __init__(self):
        """Simulate the NPK sensor, generating nitrogen, phosphorus and potassium values"""
        self.batery = 100.0
    
    def get_batery(self)->float: return self.batery   

    def simulate_npk(self)->tuple:
        """Simulates the nitrogen, phosphorus and potassium metrics in high, medium, low fertile soil"""
        self.batery -= 0.2
        n = random.randint(90, 251)
        
        if n >= 150:
            p = random.randint(40, 61)
            k = random.randint(200, 301)
            
        elif (n >= 120 and n < 150):
            p = random.randint(20, 41)
            k = random.randint(150, 201)

        elif (n >= 90 and n < 120):
            p = random.randint(10, 21)
            k = random.randint(100, 151)
        
        return n, p, k
