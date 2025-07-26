import logging

## configure logging setting
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('app1.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Arithmetic_App")

def add(a,b):
    result = a+b
    logger.debug(f'Adding {a}+{b} = {result}')
    return result

def sub(a,b):
    result = a-b
    logger.debug(f'Subtracting {a}-{b} = {result}')
    return result

def multiply(a,b):
    result = a*b
    logger.debug(f'Multiplying {a}*{b} = {result}')
    return result

def division(a,b):
    try:
        result = a/b
        logger.debug(f'Dividing {a}/{b} = {result}')
        return result
    except ZeroDivisionError:
        logger.error("Division by zero error")
        return None
    
print(add(10,20))
print(sub(23,10))
print(multiply(23,7))
print(division(20,10))
print(division(7, 0))