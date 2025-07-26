from logger import logging

def add(a, b):
    logging.debug('Performing Addition')
    return a+b

logging.debug('Calling addition method')
add(10,12)