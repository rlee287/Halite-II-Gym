import math
# Derived with sympy
def wilson_binom(z,n,p):
    b=(n*p - n*z*math.sqrt(-4*n*p*(p - 1) + z**2)/(2*abs(n)) + z**2/2)/(n + z**2)
    t=(n*p + n*z*math.sqrt(-4*n*p*(p - 1) + z**2)/(2*abs(n)) + z**2/2)/(n + z**2)
    return (b,t)

def wilson_binom_top(z,n,p):
    #b=(n*p - n*z*math.sqrt(-4*n*p*(p - 1) + z**2)/(2*abs(n)) + z**2/2)/(n + z**2)
    t=(n*p + n*z*math.sqrt(-4*n*p*(p - 1) + z**2)/(2*abs(n)) + z**2/2)/(n + z**2)
    return t

Z_95p =1.6448536269514722
Z_975p=1.959963984540054

