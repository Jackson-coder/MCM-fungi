import numpy as np
import matplotlib.pyplot as plt
import dataset
import Q1

# fs = open('福克斯.csv', 'r')
# temperature,Humidity = dataset.import_data(fs)



# 参数设计
np.set_printoptions(precision=2)
temperature_low = np.random.normal(loc=20, scale=15, size=50)
temperature_high = temperature_low+np.random.normal(loc=40, scale=15, size=50)
width_low = np.random.normal(loc=30, scale=8, size=50)/100
width_high = width_low+np.random.normal(loc=50, scale=8, size=50)/100
extension_rate = np.random.normal(loc=50, scale=15, size=50)/100

moisture_tolerance = np.random.normal(loc=50, scale=15, size=50)
decomposition_rate = np.random.normal(loc=15, scale=5, size=50)/100


# temperature_now = temperature[0]
# width_now = Humidity[0]
temperature_now = 27
width_now = 0.25
number_now = np.random.normal(loc=10, scale=2, size=50)
number_now = np.around(number_now)

print("temperature_low",temperature_low)
print("temperature_high",temperature_high)
print("width_low",width_low)
print("width_high",width_high)
print("extension_rate",extension_rate)
print("moisture_tolerance",moisture_tolerance)
print("decomposition_rate",decomposition_rate)
# print("temperature_now",temperature_now)
# print("width_now",width_now)
print("number_now",number_now)

fnus = []
K = 800000
m2 = 16000
for i in range(50):
    fnu = Q1.fnugis(extension_rate[i], temperature_high[i],
                    temperature_low[i], temperature_now, \
                        width_high[i], width_low[i], width_now, 0.006, 0.004, \
                            number_now[i], K, moisture_tolerance[i], decomposition_rate[i])
    fnus.append(fnu)

number=[]
decomposition=[]
extension_rate=[]
litter=[]

#training
for i in range(5000):
    # for j in range(50):
        # fnus[j].T_real = temperature[i]
        # fnus[j].W_real = Humidity[i]

    total_number,total_decomposition_rate,m2,d_number  = Q1.update_real_number(fnus,m2)

    number.append(total_number)
    decomposition.append(total_decomposition_rate)
    extension_rate.append(d_number)
    litter.append(m2)


plt.subplot(2,2,1)
plt.xlabel('t/h')
plt.ylabel('extension rate')
plt.title('The Extension rate Along With Time')
plt.plot(extension_rate)

plt.subplot(2,2,2)
plt.xlabel('t/h')
plt.ylabel('amount of fnugis')
plt.title('The Amount of Whole Species of Fnugis Along With Time')
plt.plot(number)

plt.subplot(2,2,3)
plt.xlabel('t/h')
plt.ylabel('amount of fnugi')
plt.title('The Amount of ALl Random Fnugis Along With Time')
for i in range(len(fnus)):
    plt.plot(fnus[i].number_log)

plt.subplot(2,2,4)
plt.xlabel('t/h')
plt.ylabel('acceration of fnugi growth')
plt.title('The Acceration of ALl Random Fnugis Along With Time')
for i in range(len(fnus)):
    plt.plot(fnus[i].dnumber_log)
plt.show()

plt.subplot(1,2,1)
plt.xlabel('t/h')
plt.ylabel('decomposition')
plt.title('The Decomposition Along With Time')
plt.plot(decomposition)

plt.subplot(1,2,2)
plt.xlabel('t/h')
plt.ylabel('the left of the litter')
plt.title('The Litter Left Along With Time')
plt.plot(litter)
plt.show()


plt.xlabel('extension_rate')
plt.ylabel('decomposition')
plt.title('The Decomposition Along With Extension_rate')
plt.plot(extension_rate,decomposition)
plt.show()

# plt.subplot(1,2,1)
# plt.xlabel('t/h')
# plt.ylabel('temperature(℃)')
# plt.title('The Temperature Along With Time')
# plt.plot(temperature)

# plt.subplot(1,2,2)
# plt.xlabel('t/h')
# plt.ylabel('Humidity')
# plt.title('The Humidity Along With Time')
# plt.plot(Humidity)
# plt.show()
