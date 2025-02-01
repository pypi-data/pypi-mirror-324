import math as m

# Constants
def pi():
    return 3.141592653589793

def e():
    return 2.718281828459045

def tau():
    return 2*pi()

#Use after in the code
def abs(x):
    return x.__abs__()

# Operation on lists
def zero(number):
    return [0]*number

def prod(L, a):
    return [a*i for i in L]

def add_list(*args):
    if not args:
        return []
    result=zero(max(len(lst) for lst in args))
    for lst in args:
        if type(lst)==list:
            for i in range(len(lst)):
                result[i]+=lst[i]
    return result

def add(L1, L2):
    if len(L1)==len(L2):
        return [L1[i]+ L2[i] for i in range(len(L1))]
    else:
        return add_list(L1, L2)

def linespace(start, end, step=1):
    step=abs(step) if start<end else -abs(step)
    return [i for i in range(start, end+(1 if step>0 else -1), step)]

def array(start, end, n):
    if n<=0:
        return []
    return [start+i*(end-start)/n for i in range(n)]

def uniwd(*listes):
    resultat=[]
    for liste in listes:
        for element in liste:
            if element not in resultat:
                resultat.append(element)
    return resultat

def inter(*listes):
    return list(set(listes[0]).intersection(*listes[1:]))

def uniq(L):
    return list(set(L))

def moy(L):
    if len(L)!=0:
        return sum(L)/len(L)
    else:
        return None

def sum_int(start, end):
    return sum(linespace(start, end))

# Mathematical operations

def cos(x):
    return m.cos(x)

def sin(x):
    return m.sin(x)

def log(x, base):
    if x>0:
        return m.log(x, base)
    
def exp(x):
    return m.exp(x)

def sqrt(x):
    if x>=0:
        return m.sqrt(x)
    else:
        return None

def facto(n):
    if n>=1:
        n=int(n)
        for i in range(2, n):
            n*=i
        return n
    else:
        return 1

def floor(x):
    if x>=0:
        return int(x)
    else:
        return int(x)-1

def ceil(x):
    if x>=0:
        return int(x)+1
    else:
        return int(x)
    
def rint(x):
    if abs(x-floor(x))<=abs(x-ceil(x)):
        return floor(x)
    else:
        return ceil(x)

# Logical operations
def binr(x):
    return bin(x)[2:]

def changement_base(valeur, inp_base, out_base)->int: 
    if valeur>0:
        puissance=int(m.log(valeur)/m.log(out_base))
        reste=valeur-out_base**puissance
        binaire=inp_base**puissance
        return binaire+changement_base(reste, inp_base, out_base)
    else:
        return 0

def divisor_list(n):
    list_div=[]
    for i in range(1, n+1):
        if n%i==0:
            list_div.append(i)
    return list_div

def gcd(r1, r0):
    while r0!=0 and r1!=0: r0, r1=r1, r0%r1
    return r0

def dicho(a, b, f, eps):
    while b-a>eps: 
        if f(a)*f((a+b)/2)<0 or f(b)*f((a+b)/2)>0:
            (a, b)=(a, (a+b)/2) 
        else:
            (a, b)=((a+b)/2, b)
    return (a+b)/2

def size(point_A, point_B):
    return ((point_A[0]-point_B[0])**2+(point_A[1]-point_B[1])**2)**(1/2)
