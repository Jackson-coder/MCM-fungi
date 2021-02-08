import numpy as np
import matplotlib.pyplot as plt
import dataset
import Q1
import copy


def draw(extension_rate, number, fnus, decomposition, temperature, Humidity):
    plt.subplot(2, 3, 1)
    plt.xlabel('t/day')
    plt.ylabel('extension speed')
    plt.title('The Extension Speed Along With Time')
    plt.plot(extension_rate)

    plt.subplot(2, 3, 2)
    plt.xlabel('t/day')
    plt.ylabel('amount of fungi')
    plt.title('The Amount of Whole Fungi Along With Time')
    plt.plot(number)

    plt.subplot(2, 3, 3)
    plt.xlabel('t/day')
    plt.ylabel('amount of fungi')
    plt.title('The Amount of All Fungi Along With Time')
    for i in range(len(fnus)):
        plt.plot(fnus[i].number_log)

    plt.subplot(2, 3, 4)
    plt.xlabel('t/day')
    plt.ylabel('each extension speed')
    plt.title('Each Extension Speed of All fungi Along With Time')
    for i in range(len(fnus)):
        plt.plot(fnus[i].dnumber_log)

    plt.subplot(2, 3, 5)
    plt.xlabel('t/day')
    plt.ylabel('temperature(℃)')
    plt.title('The Temperature Along With Time')
    plt.plot(temperature[:2000])

    plt.subplot(2, 3, 6)
    plt.xlabel('t/day')
    plt.ylabel('drought index')
    plt.title('The Drought Index Along With Time')
    plt.plot(Humidity[:2000])
    plt.show()

    # plt.xlabel('extension_rate')
    # plt.ylabel('decomposition')
    # plt.title('The Decomposition Along With Extension_rate')
    # plt.plot(extension_rate, decomposition)
    # plt.show()
    return


def compare(record):
    cities = ['Manaus', 'Los Angeles', 'Focus', 'Turpan', 'Seattle']

    plt.xlabel('t/day')
    plt.ylabel('decomposition')
    plt.title('The Decomposition Along With Time')
    l = []
    for i in range(len(cities)):
        decomposition, litter, record_x, record_y = record[i]
        L, = plt.plot(decomposition)
        l.append(L,)
    plt.legend(handles=l, labels=cities, loc='best')
    plt.show()

    plt.xlabel('t/day')
    plt.ylabel('the left of the woody fibers')
    plt.title('The Woody Fibers Left Along With Time')
    l = []
    for i in range(len(cities)):
        decomposition, litter, record_x, record_y = record[i]
        L, = plt.plot(litter)
        l.append(L,)
        plt.plot(record_x, record_y, 'x')
        print(record_x)
    plt.legend(handles=l, labels=cities, loc='best')
    plt.show()

    return


def record_experment_data(fs, fnus):

    # print(fnus[0].Neq)
    m2 = 800000
    threshold = 400000

    temperature, Humidity = dataset.import_data(fs)
    # temperature = np.random.normal(loc=0, scale=3, size=7000)
    # Humidity = np.random.normal(loc=0.5, scale=0.1, size=7000)

    number = []
    decomposition = []
    extension_rate = []
    litter = []

    record_x = []
    record_y = []
    # training
    for i in range(5000):
        for j in range(len(fnus)):
            fnus[j].T_real = temperature[i]
            fnus[j].W_real = Humidity[i]

        total_number, total_decomposition_rate, m2, d_number, flag, threshold = Q1.update_real_number(
            fnus, m2, threshold)

        number.append(total_number)
        decomposition.append(total_decomposition_rate)
        extension_rate.append(d_number)
        litter.append(m2)
        if flag == 1:
            record_x.append(i)
            record_y.append(threshold*2)
        # plt.plot()
        # plt.show()
    return extension_rate, number, fnus, decomposition, litter, record_x, record_y, temperature, Humidity


# 参数设计
size = 30
np.set_printoptions(precision=2)
temperature_low = np.random.normal(loc=0, scale=10, size=size)
temperature_high = np.random.normal(loc=20, scale=10, size=size)
for i in range(size):
    if temperature_high[i] < 0:
        temperature_high[i] = 3
temperature_high = temperature_low + temperature_high

temperature = (temperature_high + temperature_low) / 2

width_low = np.random.normal(loc=4, scale=2, size=size) / 10
for i in range(size):
    if width_low[i] < 0:
        width_low[i] = 1e-07

width_high = np.random.normal(loc=10, scale=4, size=size) / 10
for i in range(size):
    if temperature_high[i] < 0:
        temperature_high[i] = 0.5
width_high = width_high + width_low

width = (width_high + width_low) / 2

extension_rate = np.random.normal(loc=50, scale=15, size=size)/100
moisture_tolerance = np.random.normal(loc=50, scale=15, size=size)
decomposition_rate = np.random.normal(loc=15, scale=5, size=size)/100

# 定义竞争因子
competition_a = np.random.normal(loc=50, scale=15, size=size)/100

# 定义共生因子
flag = 0
symbiosis_b = np.zeros(size)
symbiosis_index = np.zeros(size)

# 定义寄生因子
f_flag = 0
parasitic_c = np.zeros(size)
parasitic_index = np.zeros(size)
be_parasitic_index = np.zeros(size)


for i in range(size):
    for j in range(size):
        if i != j and i != 0 and j != 0 and abs(temperature[i]-temperature[j]) < 5 and abs(width[i] - width[j]) < 0.4:
            flag += 1
            symbiosis_b[i] = 0.2
            symbiosis_index[i] = j
            symbiosis_b[j] = 0.1
            symbiosis_index[j] = i
            if flag == 2:
                break
    if flag == 2:
        break


for i in range(int(size/2)):
    for j in range(int(size/2)):
        if i != j and abs(temperature[int(size/2)+i]-temperature[int(size/2)+j]) < 5 and abs(width[int(size/2)+i] - width[int(size/2)+j]) < 0.4:
            f_flag += 1
            parasitic_c[int(size/2)+i] = 0.1
            parasitic_index[int(size/2)+i] = int(size/2)+j
            be_parasitic_index[int(size/2)+j] = int(size/2)+i
            break
    if f_flag == 1:
        break


for i in range(size):
    if extension_rate[i] <= 0:
        extension_rate[i] = 0.01
    if moisture_tolerance[i] <= 0:
        moisture_tolerance[i] = 40
    if decomposition_rate[i] <= 0:
        decomposition_rate[i] = 0.10
    if competition_a[i] <= 0:
        competition_a[i] = 0.5


# temperature_now = temperature[0]
# width_now = Humidity[0]
temperature_now = 27
width_now = 0.25

# number_now = np.random.normal(loc=10, scale=2, size=50)
# number_now = np.around(number_now)

number_now = []
for i in range(size):
    number_now.append(np.random.randint(5, 15))

print("temperature_low", temperature_low)
print("temperature_high", temperature_high)
print("width_low", width_low)
print("width_high", width_high)
print("extension_rate", extension_rate)
print("moisture_tolerance", moisture_tolerance)
print("decomposition_rate", decomposition_rate)
print("number_now", number_now)

# temperature_low = np.array([  7.65,   5.4,   10.75, -12.64,  -0.84,   2.88 , -9.63,  -1.78, -14.84,  -3.18,
#    3.47,  -0.98 , -1.67 , -0.37,   4.45  , 3.42  , 3.32 ,-25.95, -15.95,  -1.49,
#   14.97 , 18.04 ,  4.47 , 19.59 , -6.17 ,  6.66, -10.52 ,  1.37 , -5.66 , -8.6,
#  -15.26 , -0.99  ,-0.83 ,28.56 , -4.17 ,  6.59 , -4.93 , -6.14 , -8.32 ,  9.49,
#  -11.84 , 16.15 ,-17.78 ,-14.45 , -6.09 ,-18.98 , -1.44 ,-12.43 , -8.26, -13.8 ])
# temperature_high = np.array([ 24.33 , 25.02 , 36.59 ,  6.57 , 12.67 ,  5.2  ,  6.96  , 0.5   , 0.5 ,  12.67,
#   23.49 , 22.54  , 7.56 , 20.62 , 33.88 , 14.03 , 40.19 ,  0.5  ,  0.5   , 2.83,
#   71.18 , 25.64 , 31.68  ,45.83,  13.9 ,  18.24,   0.5  , 33.75 , 35.8 ,   0.5,
#   13.07 , 17.59 , 21.87 , 58.64 , 18.08 , 26.06 , 28.25 , 13.01 , 26.16 , 29.77,
#   16.92 , 47.29 ,  0.5  ,  0.5 ,  15.23 , 17.52 , 18.89 , 10.91 ,  2.05 ,  0.5 ])
# temperature = (temperature_high + temperature_low) / 2
# width_low = np.array([ 0.22,  0.6  , 0.47,  0.51 , 0.42 , 0.31 , 0.61 , 0.47 , 0.26 , 0.17 , 0.15,  0.24,
#   0.26 , 0.77 , 0.09 , 0.82,  0.1  , 0.4  , 0.4 ,  0.48 , 0.32 , 0.44,  0.38 , 0.57,
#   0.64 , 0.24 , 0.39 , 0.41 , 0.22 , 0.46 , 0.47 , 0.38 , 0.56,  0.2 ,  0.43 , 0.04,
#   0.18 , 0.24 , 0.32 , 0.29 , 0.36 , 0.68 , 0.23  ,0.3 ,  0.2 ,  0.64 , 0.22 , 0.25,
#   0.5 ,  0.3 ])
# width_high = np.array([ 0.89 , 1.45 , 1.72 , 1.21 , 1.02 , 0.74 , 1.34 , 1.55 , 1.67 , 0.77,  1.23 , 0.9,
#   1.5  , 2.03 , 0.66 , 2.53 , 1.02 , 1.75  ,1.53 , 1.09 , 0.63 , 1.18  ,1.49  ,1.35,
#   1.58 , 1.35 , 1.21,  1.21 , 1.13,  1.58 , 1.86,  1.13,  1.59 , 1.34,  1.58 , 0.79,
#   1.53 , 1.9  , 0.77 , 1.33 , 1.37 , 2.22,  0.53 , 1.49  ,1.16 , 0.91 , 1.11 , 1.05,
#   1.73 , 2.24])
# width = (width_high + width_low) / 2
# extension_rate = np.array([ 0.52 , 0.34 , 0.71,  0.32 , 0.35 , 0.26 , 0.7 ,  0.41 , 0.61 , 0.57,  0.59 , 0.19,
#   0.73 , 0.47 , 0.68 , 0.45 , 0.51 , 0.59 , 0.36 , 0.2  , 0.18 , 0.57 , 0.28 , 0.68,
#   0.57 , 0.49 , 0.1  , 0.36 , 0.36 , 0.5  , 0.54 , 0.28 , 0.37 , 0.53 , 0.46 , 0.36,
#   0.53 , 0.31  ,0.6 ,  0.55 , 0.42 , 0.33 , 0.54 , 0.48 , 0.5  , 0.47 , 0.28 , 0.67,
#   0.51 , 0.77])
# moisture_tolerance =  np.array([ 12.41,  45.86,  30.77 , 60.84 , 59.43 , 62.63 , 28.16 , 31.57 , 38.6 ,  65.45,
#   59.53 , 12.1 ,  65.19 , 49.37 , 25.04 , 46.27 , 47.4  , 44.09 , 45.42 , 36.07,
#   35.98 , 46.82 , 43.69 , 15.98,  66.11 , 52.19 , 48.7 ,  45.42 , 67.07 , 63.71,
#   16.3  , 26.32 , 44.16 ,66.98 , 62.37 , 64.78,  46.27 , 48.  ,  60.9  , 40.12,
#   68.57 , 29.53 , 19.63 , 38.24 , 59.66 , 42.38 , 37.38 , 17.62 , 50.97 , 36.06])
# decomposition_rate =  np.array([ 0.1  , 0.08  ,0.14 , 0.17,  0.14 , 0.08,  0.13 , 0.14 , 0.1  , 0.25 , 0.13,  0.15,
#   0.17 , 0.17  ,0.12,  0.06 , 0.15,  0.13,  0.23 , 0.2  , 0.15 , 0.14 , 0.16 , 0.16,
#   0.12 , 0.21  ,0.17 , 0.23 , 0.09 , 0.12 , 0.14 , 0.21 , 0.19 , 0.09 , 0.08,  0.15,
#   0.05 , 0.19 , 0.12 , 0.13  ,0.11 , 0.2  , 0.09 , 0.13 , 0.18 , 0.11  ,0.15 , 0.14,
#   0.19 , 0.09])
# number_now =  np.array([8, 6, 10, 14, 11, 7, 12, 5, 13, 12, 11, 9, 14, 14, 5, 5, 9, 12, 6, 13, 9, 12, 6, 7, 5, 10, 10, 7, 11, 5, 5, 10, 12, 7, 5, 5, 7, 8, 5, 6, 8, 6, 10, 9, 14, 6, 5, 14, 12, 5])
# competition_a =  np.array([ 0.32 , 0.42 , 0.25 , 0.37 , 0.54 , 0.37 , 0.43 , 0.44 , 0.55 , 0.67 , 0.43 , 0.4,
#   0.43 , 0.41 , 0.51 , 0.66 , 0.37 , 0.42 , 0.18 , 0.4 ,  0.3  , 0.52 , 0.58 , 0.47,
#   0.52 , 0.42,  0.33 , 0.52,  0.64 , 0.32  ,0.49 , 0.5 ,  0.66 , 0.58 , 0.39 , 0.31,
#   0.49 , 0.27 , 0.63,  0.29 , 0.53 , 0.6  , 0.41 , 0.61 , 0.72 , 0.31,  0.5 ,  0.36,
#   0.11 , 0.56])
# symbiosis_b =  np.array([ 0.  , 0.002 , 0. ,  0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.  , 0.001 , 0.   ,0. ,  0.  , 0.,
#   0. ,  0. ,  0. ,  0.  , 0.  , 0.  , 0.  , 0.1 , 0. ,  0. ,  0. ,  0. ,  0. ,  0.  , 0.,
#   0. ,  0.  , 0. ,  0.  , 0. ,  0.  , 0.   ,0. ,  0. ,  0.   ,0. ,  0.  , 0. ,  0. ,  0.,
#   0. ,  0. ,  0.  , 0.,   0. ])
# symbiosis_index =  np.array([  0. , 22. ,  0. ,  0.  , 0.  , 0. ,  0.  , 0. ,  0. ,  0. ,  1.,   0. ,  0. ,  0.,   0.,
#    0. ,  0. ,  0.  , 0.  , 0.  , 0. ,  0. ,  1. ,  0.  , 0.   ,0. ,  0.,   0.  , 0. ,  0.,
#    0.  , 0.  , 0. ,  0. ,  0.  , 0. ,  0. ,  0.  , 0. ,  0. ,  0.  , 0.  , 0. ,  0.,   0.,
#    0.  , 0. ,  0. ,  0.,   0.])
# parasitic_c =  np.array([ 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0.,  0.,  0.,
#   0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. ,
#   0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0. , 0.])
# parasitic_index =  np.array([  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , 0. ,  0. ,  0. ,  0.,
#    0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , 0. ,  0. ,  0. ,  0. ,  0.,
#    0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.,
#    0. ,  0. ,  0. ,  0. ,  0.])
# be_parasitic_index =  np.array([  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , 0. ,  0. ,  0. ,  0.,
#    0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. , 0. ,  0. ,  0. ,  0. ,  0.,
#    0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.,
#    0. ,  0. ,  0. ,  0. ,  0.])
# size = 50


F = []
K = 800000
temperature_now = 5.89
width_now = 0.375

for i in range(size):
    fnu = Q1.fungis(extension_rate[i], temperature_high[i],
                    temperature_low[i], temperature_now,
                    width_high[i], width_low[i], width_now, 0.00035, 0.015,
                    number_now[i], K, moisture_tolerance[i], decomposition_rate[i], competition_a[i], symbiosis_b[i], symbiosis_index[i], parasitic_c[i], parasitic_index[i], be_parasitic_index[i])
    F.append(fnu)

file_csv = ['Manaus.csv', 'Los Angeles.csv',
            'Focus.csv', 'Turpan.csv', 'Seattle.csv']

# file_csv = ['Seattle.csv']

litter_record = []
for csv in file_csv:
    fs = open(csv, 'r')
    fnus = copy.deepcopy(F)
    extension_rate, number, fnus, decomposition, litter, record_x, record_y, temperature, Humidity = record_experment_data(
        fs, fnus)

    draw(extension_rate, number, fnus, decomposition, temperature, Humidity)

    litter_record.append([decomposition, litter, record_x, record_y])

L1 = []
L2 = []

compare(litter_record)
