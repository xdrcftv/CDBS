from text_parser import *

CDBS_path = 'C:/Users/user/Desktop/CDBS/'

P_A_dir = '/Polymer_A'
P_B_dir = '/Polymer_B'
s_1_dir = '/sample_1'
s_2_dir = '/sample_2'
s_3_dir = '/sample_3'
XP151_dir = '/XP151'


P_A_data, P_A_point = sudo_normalize(asc_parser(CDBS_path+P_A_dir))
P_B_data, P_B_point = sudo_normalize(asc_parser(CDBS_path+P_B_dir))
s_1_data, s_1_point = sudo_normalize(asc_parser(CDBS_path+s_1_dir))
s_2_data, s_2_point = sudo_normalize(asc_parser(CDBS_path+s_2_dir))
s_3_data, s_3_point = sudo_normalize(asc_parser(CDBS_path+s_3_dir))
XP151_data, XP151_point = sudo_normalize(asc_parser(CDBS_path+XP151_dir))



B_index = 267

# channel_number = np.arange(1023)
#
channel_range = 15
x = np.arange(A_index-channel_range, A_index+channel_range)
plt.plot(x, interest_data[B_index, A_index-channel_range:A_index+channel_range])
plt.title('XP151_data')
plt.xlabel('channel number')
plt.ylabel('counts')
plt.show()

# plt.imshow(CDBS_data)
# plt.show()
#

# max_value = np.amax(CDBS_data)
# r, c = np.where(CDBS_data == max_value)
# print(r,c)
# print(CDBS_data[r][c])
# print(len(CDBS_data[0]))
