import random as rand

# Operation on lists
def zero(number: int)->list[int]:
    return [0]*number

def prod(L: list[int|float], a: int|float)->list[int|float]:
    return [a*i for i in L]

def addl(*args: list[int|float])->list[int|float]:
    if not args:
        return []
    result=zero(max(len(lst) for lst in args))
    for lst in args:
        if type(lst)==list:
            for i in range(len(lst)):
                result[i]+=lst[i]
    return result

def linespace(start: int, end: int, step=1)->list[int|float]:
    step=(step).__abs__() if start<end else -(step).__abs__()
    return [i for i in range(start, end+(1 if step>0 else -1), step)]

def array(start: int|float, end: int|float, n: int)->list[int|float]:
    if n<=0:
        return []
    return [start+i*(end-start)/n for i in range(n+1)]

def uni(*lists: list)->list:
    return [item for lst in lists for item in lst]

def uniwd(*listes: list)->list:
    resultat=[]
    for liste in listes:
        for element in liste:
            if element not in resultat:
                resultat.append(element)
    return resultat

def inter(*listes: list)->list:
    return list(set(listes[0]).intersection(*listes[1:]))

def uniq(L: list)->list:
    return list(set(L))

def moy(L: list[int|float])->int|float:
    if len(L)!=0:
        return sum(L)/len(L)
    else:
        return float('nan')

def sum_int(start: int, end: int)->int:
    return sum(linespace(start, end))

def randl(min: int|float, max: int|float, n: int)->list[int|float]:
    return [rand.randint(min, max) for i in range(n)]

def shuffle_list(L: list)->list:
    L_=L[:]
    rand.shuffle(L_) 
    return L_

def filtrer(L: list, condition: callable)->list:
    return [x for x in L if condition(x)]

def apply(L: list, fonction)->list:
    return [fonction(i) for i in L]

def chunk(L: list, n: int)->list[list]:
    if n>=1:
        return [L[i:i+n] for i in range(0, len(L), n)]
    else:
        raise ValueError("n must be greater than or equal to 1")

def partition(L: list, condition: callable)->tuple:
    if callable(condition):
        return [x for x in L if condition(x)], [x for x in L if not condition(x)]
    else:
        raise ValueError("Condition must be a function")
