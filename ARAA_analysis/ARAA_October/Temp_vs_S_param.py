import matplotlib.pyplot as plt

temp = [300, 600, 700, 800, 900, 1000, 1050]
S_param = [0.492, 0.492, 0.487, 0.487, 0.483, 0.479, 0.487]


plt.plot(temp, S_param, '^--')
plt.title('S parameter')
# plt.xlim(0, 15)
# plt.ylim(0.85, 1.40)
plt.xlabel("Temperature [K]")
plt.ylabel("S parameter [A.U.]")
plt.legend(loc='best')
plt.show()