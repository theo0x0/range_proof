from range_create import g, create, order, bits

powers = [2**i for i in range(bits)]


rp = create()

V  = rp[0]
R = rp[1]
R2 = rp[2]
LR = rp[3]
RR = rp[4]
s = rp[5]
s1 = rp[6]
s2 = rp[7]

a = V.x + R2.x
powers_of_2 = [2**i for i in range(bits)]
one_s_neg = [1] * bits
one_s = [1] * bits


for i in range(5):
    if not LR[i].is_infinity:
        a += LR[i].x
    if not RR[i].is_infinity:
        a += RR[i].x
        
        
    V += a*LR[i] + pow(a,-1,order)*RR[i]
    
    for ii in range(bits):
        if ii & powers[i]:
            one_s_neg[ii] *= pow(a,-1,order)
            powers_of_2[ii] *= pow(a,-1,order)
            one_s[ii] *= a
            
    
a += R.x 

print(sum(one_s)*s1 *g[0] + sum(one_s_neg)*s2*g[1] + s2*(s1-sum(powers_of_2))*g[2] == V + a*R + a*a*R2 + s*g[3])



