import matplotlib.pyplot as plt

####################################### plt control ################################################
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 15

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=15)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
####################################### plt control ################################################

# label_list = ['13C', 'TMP21', 'TMP22', 'TMP38', 'TMP24', 'TMP41', 'TMP34', 'TMP27']
label_list = ['TMP21', 'TMP22', 'TMP38', 'TMP24', 'TMP41', 'TMP34', 'TMP27']
temp = [300, 400, 500, 600, 650, 700, 750]
# s_param = [0.4923028235542439, 0.4915950008065062, 0.4867559238114307, 0.4869692600315476,
#            0.4838170415546046, 0.49072704640787407, 0.49004602136196380, 0.48391269655250135]
s_param = [0.4915950008065062, 0.48395642187823495, 0.48112911440454836,
           0.4838170415546046, 0.49072704640787407, 0.49004602136196380, 0.48391269655250135]
m_lifetime = [0.175, 0.165, 0.163, 0.164, 0.174, 0.168, 0.166]

fig, ax1 = plt.subplots()
ax1.set_xlabel('T(Celsius)')
ax1.set_ylabel('S')
ax1.plot(temp, s_param, 'o--', color='green', label='CDBS')
# ax1.plot(temp, s_param, 'o', label='CDBS')
ax1.legend(loc='upper right')
# for i in range(len(label_list)):
#     plt.plot(temp[i], s_param[i], 'o', label=label_list[i])
ax2 = ax1.twinx()
ax2.set_ylabel('Mean Lifetime')
ax2.plot(temp, m_lifetime, '^--', color='deeppink', label='PALS')
ax2.legend(loc='lower right')

plt.title('25% HR')

plt.show()