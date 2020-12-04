import matplotlib.pyplot as plt

label_list = ['13C', 'TMP21', 'TMP22', 'TMP38', 'TMP24', 'TMP34']
temp = [200, 300, 400, 500, 600,700]
s_param = [0.4923028235542439, 0.4915950008065062, 0.4867559238114307, 0.4869692600315476,
           0.4834340377120744, 0.47869561167497593]

for i in range(len(label_list)):
    plt.plot(temp[i], s_param[i], 'o', label=label_list[i])

plt.title('25% HR')
plt.xlabel('T (Celsius)')
plt.ylabel('S')
plt.legend(loc='best')
plt.show()