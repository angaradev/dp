import string
import random

def random_string_generator(size=4, chrs=string.digits):
    return "DP-" + ''.join(random.choice(chrs) for _ in range(size)) 
