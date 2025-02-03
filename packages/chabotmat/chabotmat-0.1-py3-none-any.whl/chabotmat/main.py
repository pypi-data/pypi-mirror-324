import numpy as np
import random as rd


# ----------------------------------------------------------------------------------

def derive(f, x, dx=1e-6):
    return (f(x+dx)-f(x))/dx

# ----------------------------------------------------------------------------------

def Newton(f,a,b,N):
    assert f(a)*f(b)<0, "Invalid interval"

    def phi(x):
        return x - (f(x)/derive(f,x))
    
    if f(a)<f(b): u=b
    elif f(a)>f(b): u=a
    else: return False

    for _ in range(N):
        u = phi(u)

    return u

# ----------------------------------------------------------------------------------

def Dicho(f,a,b,eps):
    
    def g(x):
      return f(a)*f(x)

    assert g(a)*g(b)<0 and b-a > 0, "Invalid interval"


    while b-a>eps:
        m = (b+a)/2

        if g(a)*g(m) < 0: b=m
        else: a=m

    return (b+a)/2


# ----------------------------------------------------------------------------------

def MonteCarlo(N, f, mes:list, u_mes:list):

    evals = []
    for _ in range(N):

        res = []
        for i in range(len(mes)):
            res.append(rd.uniform(mes[i]-u_mes[i], mes[i]+u_mes[i]))
        
        evals.append(f(res))

    return evals

# ----------------------------------------------------------------------------------

