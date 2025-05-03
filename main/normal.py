import math
import random

def normal(media, desviacion):
    rnd1 = random.random()
    rnd2 = random.random()
    num1 = (((math.sqrt(-2 * math.log(rnd1))) * math.cos(2 * math.pi * rnd2)) * desviacion) + media
    num2 = (((math.sqrt(-2 * math.log(rnd1))) * math.sin(2 * math.pi * rnd2)) * desviacion) + media
    return num1, num2