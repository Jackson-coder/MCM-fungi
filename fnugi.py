import numpy as np
import matplotlib.pyplot as plt
import Q1

# 参数设计
np.set_printoptions(precision=2)
temperature_low = np.random.normal(loc=20, scale=15, size=50)
temperature_high = temperature_low+np.random.normal(loc=40, scale=15, size=50)
width_low = np.random.normal(loc=20, scale=8, size=50)
width_high = width_low+np.random.normal(loc=30, scale=8, size=50)
extension_rate = np.random.normal(loc=50, scale=15, size=50)/100

moisture_tolerance = np.random.normal(loc=50, scale=15, size=50)
decomposition_rate = np.random.normal(loc=15, scale=5, size=50)/100


temperature_now = np.random.normal(loc=27, scale=5, size=50)
width_now = np.random.normal(loc=25, scale=5, size=50)
number_now = np.random.normal(loc=10, scale=2, size=50)
number_now = np.around(number_now)
# number_now = []
# for i in range(50):
#     number_now.append (1)
# number_now = np.array(number_now)

print("temperature_low",temperature_low)
print("temperature_high",temperature_high)
print("width_low",width_low)
print("width_high",width_high)
print("extension_rate",extension_rate)
print("moisture_tolerance",moisture_tolerance)
print("decomposition_rate",decomposition_rate)
print("temperature_now",temperature_now)
print("width_now",width_now)
print("number_now",number_now)

fnus = []
K = 800000
m2 = 16000
for i in range(50):
    fnu = Q1.fnugis(extension_rate[i], temperature_high[i],
                    temperature_low[i], temperature_now[i], \
                        width_high[i], width_low[i], width_now[i], 0.006, 0.004, \
                            number_now[i], K, moisture_tolerance[i], decomposition_rate[i])
    fnus.append(fnu)

number=[]
decomposition=[]
extension_rate=[]
numii = []

for i in range(10000):
    total_number,total_decomposition_rate,m2,d_number,numi  = Q1.update_real_number(fnus,m2)

    number.append(total_number)
    decomposition.append(total_decomposition_rate)
    extension_rate.append(d_number)
    numii.append(numi)

    
    for j in range(50):
        if i == 1:
            print(fnus[j].number,end=',')
    



plt.subplot(3,2,1)
plt.plot(extension_rate)
plt.subplot(3,2,3)
plt.plot(number)
plt.subplot(3,2,5)
plt.plot(numii)
plt.subplot(1,2,2)
plt.plot(decomposition)
plt.show()

# print(extension_rate)


# total_number,total_decomposition_rate  = Q1.update_real_total_number(fnus)
# print(total_number,total_decomposition_rate)




