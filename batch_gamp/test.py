'''
P0=24107523.908
L0=126685892.6421
D0=-4195.910
P1=24108405.598
L1=126690526.4181
D1=-4198.120
#P0=21788895.586
#L0=114501422.737
#D0=-2529.398

#L1=114577483.864
#P1=21803368.922
#D1=-2541.199
lam=0.19029367279836487
ns=2
Pn = 1 / ns*P1 + (ns - 1) / ns*(P0 + lam*(L1 - L0))
Pd = 1 / ns*P1 + (ns - 1) / ns*(P0 - 0.5* lam*(D1 +D0))
print(P1)
print(Pn)
print(Pd)
print(lam*(L1 - L0))
print(0.5* lam*(D1 +D0))
'''


import numpy as np

import matplotlib.pyplot as plt

t= np.arange(1000)/100.

x = np.sin(2*np.pi*10*t)

y = np.cos(2*np.pi*10*t)

fig=plt.figure()

ax1 = plt.subplot(211)

ax2 = plt.subplot(212)

ax1.plot(t,x)

ax2.plot(t,y)

ax1.get_shared_x_axes().join(ax1, ax2)

ax1.set_xticklabels([])

# ax2.autoscale() ## call autoscale if needed

plt.show()