##################################################################################################################################################################
#
#
#                                                       KeGen by m.s.m
#
#                                                                                                                                                                 
##################################################################################################################################################################

#Thanks for using KeGen! I reccomend using it in combo with encypting tools other than a simple password generator.

import string
import random
from random import choice
import time

def generate(length):
    letters_and_digits = string.ascii_letters + string.digits
    key = random.choice(letters_and_digits)
    for i in range(length - 1):
        key += random.choice(letters_and_digits)
    print(f"Generated key: {key}")    
    return key

def generatenumber(length):
    numbers = string.digits
    key = random.choice(numbers)
    for i in range(length - 1):
        key += random.choice(numbers)
    print(f"Generated key: {key}")

def generateletters(length):
    letters = string.ascii_letters
    key = random.choice(letters)
    for i in range(length - 1):
        key += random.choice(letters)
    print(f"Generated key: {key}")

def write_to_file(filename, key):
    with open(filename, 'w') as file:
        file.write(key)


