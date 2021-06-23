import matplotlib.pyplot as plt
import numpy as np

ge_density = 5.323
t = (np.array(range(1000))+1)/100

mu_511 = 8.1284E-02
mu_1273 = 5.0602E-02
mu_en_1273 = 0.0234
mu_en_511 = 0.02915
y = (1-np.exp(-mu_1273*ge_density*t))/(1-np.exp(-mu_511*ge_density*t))
y_en = (1-np.exp(-mu_en_1273*ge_density*t))/(1-np.exp(-mu_en_511*ge_density*t))
plt.figure()
plt.plot(t, y, label='$\mu$_tot')
plt.plot(t, y_en, label='$\mu$_en')
plt.legend(loc='best')
plt.xlabel('thickness [cm]')
plt.ylabel('$\epsilon_{1273}$/$\epsilon_{511}$')
plt.show()
plt.xlim(0,10)