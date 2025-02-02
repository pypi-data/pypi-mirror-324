import math as m

# Logical operations
def binr(x: int)->str:
    return bin(x)[2:]

def change_base(valeur: int, inp_base: int, out_base: int)->int: 
    if valeur>0:
        puissance=int(m.log(valeur)/m.log(out_base))
        reste=valeur-out_base**puissance
        binaire=inp_base**puissance
        return binaire+change_base(reste, inp_base, out_base)
    else:
        return 0

def divisor_list(n: int)->list[int]:
    list_div=[]
    for i in range(1, n+1):
        if n%i==0:
            list_div.append(i)
    return list_div

def dicho(start: int|float, end: int|float, f: callable, eps: int|float)->int|float:
    while end-start>eps: 
        if f(start)*f((start+end)/2)<0 or f(end)*f((start+end)/2)>0:
            (start, end)=(start, (start+end)/2) 
        else:
            (start, end)=((start+end)/2, end)
    return (start+end)/2

def size(point_A: list[int|float, int|float], point_B: list[int|float, int|float])->int|float:
    return ((point_A[0]-point_B[0])**2+(point_A[1]-point_B[1])**2)**(1/2)
