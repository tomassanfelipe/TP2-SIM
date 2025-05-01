import math
import random

def exponencial(lambd):
    rnd = random.random()
    n = (-1 / lambd) * math.log(1 - rnd)
    return n
