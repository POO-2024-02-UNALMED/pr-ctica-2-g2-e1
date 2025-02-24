import random

class Boleta():
    def __init__(self):
        self.id = random.randint(100000,999999)

    def __str__(self):
        return f"Boleta ID: {self.id}"