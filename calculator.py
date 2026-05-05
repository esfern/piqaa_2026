def addition(x,y):
    return x+y

def subtraction(x,y):
    return x-y

def multiplication(x,y):
    return x*y

def division(x,y):
    if y == 0:
        return float('inf') # we do it like javascript 😎
    
    return x/y
