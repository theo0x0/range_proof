from generators import order, get_generators
from random import randint

bits = 32


# Convers an int to list of 2' powers
def powers(x):
    powers = []
    for i in range(bits):
        if x & 1:
            powers.append(2**i)
        else:
            powers.append(0)
            
        x = x >> 1
        
    return powers

# Initial setup
g = get_generators(4)

n = 133
s = randint(1,order-1)
V = n*(g[0] + g[1]) - s *g[3]

n_powers = powers(n)
n_powers_neg = n_powers.copy()
n_powers_neg_2 = [n_powers[i] - 2**i for i in range(bits)]
powers_of_2 = [2**i for i in range(bits)]
one_s_neg = [1] * bits
one_s = [1] * bits

r1, r2 = randint(1, order-1), randint(1, order-1)
R2 = r1*r2*g[2]


LR = []
RR = []
a = V.x + R2.x
a_s=[]

# creating and blinding pints of extra data
for i in [1,2,4,8,16]:
    
    LR.append(0*g[0])
    RR.append(0*g[0])
    
    for ii in range(0, bits, i*2):

        LR[-1] += sum(n_powers_neg[ii:i+ii])*sum(one_s[i+ii:ii+i*2])*g[0]
        RR[-1] += sum(n_powers_neg[i+ii:ii+i*2])*sum(one_s[ii:i+ii])*g[0]
        
        RR[-1] += sum(n_powers[ii:i+ii])*sum(one_s_neg[i+ii:ii+i*2])*g[1]
        LR[-1] += sum(n_powers[i+ii:ii+i*2])*sum(one_s_neg[ii:i+ii])*g[1]
        
        RR[-1] += sum(n_powers[ii:i+ii])*sum(n_powers_neg_2[i+ii:ii+i*2])*g[2]
        LR[-1] += sum(n_powers[i+ii:ii+i*2])*sum(n_powers_neg_2[ii:i+ii])*g[2]
        
        

    s_1, s_2 = randint(1, order-1), randint(1, order-1)
    LR[-1] = LR[-1] + s_1*g[3]
    RR[-1] = RR[-1] + s_2*g[3]
    
    
    if not LR[-1].is_infinity:
        a += LR[-1].x
    if not RR[-1].is_infinity:
        a += RR[-1].x
        
    s -= a*s_1 + pow(a,-1,order)*s_2
    
    a_s.append(a)
    
    # creating verifying vectors
    for ii in range(bits):
        if ii & i:
            n_powers[ii] *= a
            one_s_neg[ii] *= pow(a,-1,order)
            
            n_powers_neg[ii] *= pow(a,-1,order)
            n_powers_neg_2[ii] *= pow(a,-1,order)
            powers_of_2[ii] *= pow(a,-1,order)
            one_s[ii] *= a
            



V_start = V
# for i in range(5):
#     V += a_s[i]*LR[i] + pow(a_s[i],-1,order)*RR[i]


# creating blinding for scalars
R = r1*sum(one_s)*g[0] + r2*sum(one_s_neg)*g[1] 
R += r1*sum(n_powers)*g[2] + r2*sum(n_powers_neg)*g[2] - r2*sum(powers_of_2)*g[2]

a += R.x
s1= sum(n_powers_neg) + a*r1
s2= sum(n_powers) + a*r2

def create():
    return V_start, R, R2, LR, RR, s, s1, s2


# print(sum(one_s)*s1 *g[0] + sum(one_s_neg)*s2*g[1] + s2*(s1-sum(powers_of_2))*g[2] == V + a*R + a*a*R2 + s*g[3])


