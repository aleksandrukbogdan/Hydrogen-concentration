# Входныеданные
import math
import numpy as np
import matplotlib.pyplot as plt

b = 15.84
K = 30 * 10 ** (-3)
T = 298
P = 10
x_i = [0.2, 0.8]
M_i = [2, 16]
L = 40
d = 1220
h = 10
S0 = 159
Ea = 23.54
E = 0.95
x_interest = 40
R = 8.3141
q = 5000
P_norm = 0.101325
ro_w = 1.20445
Tkp = 32
Pkp = 7.812
Pct = 0.101325
Tct = 293.15
Tpk = 0
Ppk = 0
M = 0
Tpr = 0
Ppr = 0
# new
T_crit = [190.55, 305.5, 369.99, 425.16, 469.77, 33.23, 126.25, 304.19]
P_crit = [4.641, 4.913, 4.264, 3.796, 3.374, 1.316, 3.396, 7.382]
M_crit = [16.042, 30.068, 44.094, 58.12, 72.146, 2.016, 28.016, 44.011]
x_crit = [31, 21, 17.40, 6.80, 4.60, 10.1, 2, 7.1]
# псевдокритические параметры
for i in range(len(T_crit)):
    Tpk += T_crit[i] * x_crit[i]
    Ppk += P_crit[i] * x_crit[i]
    M += x_crit[i] * M_crit[i]
ro_c = 10 ** 3 * M * Pct / R / Tct / 1
delta = ro_c / ro_w
P = 10
P_l = [0 for i in range(L)]
P_l[0] = P
for i in range(1, L):
    Tpr = T / Tpk
    Ppr = P / Ppk

    nu0 = 10 ** (-6) * (1.81 + 5.95 * Tpr)
    B1 = -0.67 + 2.36 / Tpr - 1.93 * Tpr ** (-2)
    B2 = 0.8 - 2.89 / Tpr + 2.65 * Tpr ** (-2)
    B3 = -0.1 + 0.354 / Tpr - 0.314 * Tpr ** (-2)
    nu = nu0 * (1 + B1 * Ppr + B2 * Ppr ** 2 + B3 * Ppr ** 3)

    Re = 17.75 * 10 ** 3 * q * delta / (d * nu)
    lam_tr = 0.067 * (158 / Re + 2 * K / d) ** 0.2
    lam = lam_tr / (E ** 2)

    a1 = -0.39 + 2.03 / Tpr - 3.16 / Tpr ** 2 + 1.09 / Tpr ** 3
    a2 = 0.0423 - 0.1812 / Tpr + 0.2124 / Tpr ** 2
    Z_sr = 1 + a1 * Ppr + a2 * Ppr ** 2
    P = math.sqrt(P ** 2 - q ** 2 * lam * delta * T * Z_sr * L / (3.32 * d ** 5))
    P_l[i] = P
P_l_H2 = [0 for i in range(L)]
f_l_H2 = [0 for i in range(L)]
c_l = [0 for i in range(L)]
Es = 23.54
S = S0 * math.exp(-Es / R / T)
ri = d / 2000
ro = ri + h / 1000
r = np.linspace(ri, ro, 100)
c_lr = [[0 for j in range(len(r))] for i in range(L)]
for i in range(L):
    P_l_H2[i] = P_l[i] * x_crit[-3]
    f_l_H2[i] = P_l_H2[i] * math.exp(b * P_l_H2[i] / (R * T))
    c_l[i] = S * math.sqrt(f_l_H2[i])
    for j in range(len(r)):
        c_lr[i][j] = c_l[i] * (math.log(ro) - math.log(r[j])) / (math.log(ro) - math.log(ri))
print(len(c_lr[39]))
x = np.linspace(x_interest, x_interest+1,2)
y = np.linspace(ri, ro, 101)
#X, Y = np.meshgrid(x, y)

Z = np.asarray(c_lr[x_interest-1]).reshape(100, 1)

print(Z)
fig, ax = plt.subplots()

ax.pcolormesh(x,y, Z)

plt.show()
