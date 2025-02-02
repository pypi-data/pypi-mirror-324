import math as m
# from rathureqpy.logic_utils import divisor_list

# Constants
def pi()->float:
    return 3.141592653589793

def e()->float:
    return 2.718281828459045

def tau()->float:
    return 2*pi()

# Mathematical operations
def abs(x: int|float)->int:
    return x.__abs__()

def cos(x: int|float)->int|float:
    return m.cos(x)

def sin(x: int|float)->int|float:
    return m.sin(x)

def log(x: int|float, base=e())->int|float:
    if x>0:
        return m.log(x, base)
    return float('nan')

def exp(x: int|float)->int|float:
    return m.exp(x)

def sqrt(x: int|float)->int|float:
    if x>=0:
        return m.sqrt(x)
    return float('nan')

def facto(n: int)->int:
    return m.factorial(n) if n >= 0 else 1

def floor(x: int|float)->int:
    if x>=0:
        return int(x)
    return int(x)-1

def ceil(x: int|float)->int:
    if x>=0:
        return int(x)+1
    return int(x)
    
def rint(x:int|float)->int:
    if abs(x-floor(x))<=abs(x-ceil(x)):
        return floor(x)
    return ceil(x)
    
def gcd(r1: int, r0: int)->int:
    while r0!=0 and r1!=0: r0, r1=r1, r0%r1
    return r0

def lcm(a: int, b: int)->int:
    return abs(a*b)//gcd(a, b) if a and b else 0

def is_prime(n: int)->bool:
    if n<=1:
        return False
    for i in range(2, int(m.sqrt(n))+1):
        if n%i==0:
            return False
    return True

# Statistical measures
def variance(L: list[int])->int|float:
    if not L:
        return None
    mean=sum(L)/len(L)
    var=sum((x-mean)**2 for x in L)/len(L)
    return var

def ecart_type(L: list[int])->int|float:
    var=variance(L)
    if var is None:
        return None
    return m.sqrt(var)

def mediane(L: list[int])->int|float:
    if not L:
        return None
    L_sorted=sorted(L)
    if len(L_sorted)%2==1:
        return L_sorted[len(L_sorted)//2]
    else:
        return (L_sorted[len(L_sorted)//2-1]+L_sorted[len(L_sorted)//2])/2
