import numpy as np
import matplotlib.pyplot as plt
import dataset
import Q1
import copy


def draw(extension_rate, number, fnus, decomposition, temperature, Humidity):
    plt.subplot(2, 3, 1)
    plt.xlabel('t/per day')
    plt.ylabel('extension rate')
    plt.title('The Extension rate Along With Time')
    plt.plot(extension_rate)

    plt.subplot(2, 3, 2)
    plt.xlabel('t/per day')
    plt.ylabel('amount of fnugis')
    plt.title('The Amount of Whole Species of Fnugis Along With Time')
    plt.plot(number)

    plt.subplot(2, 3, 3)
    plt.xlabel('t/per day')
    plt.ylabel('amount of fnugi')
    plt.title('The Amount of ALl Random Fnugis Along With Time')
    for i in range(len(fnus)):
        plt.plot(fnus[i].number_log)

    plt.subplot(2, 3, 4)
    plt.xlabel('t/per day')
    plt.ylabel('acceration of fnugi growth')
    plt.title('The Acceration of ALl Random Fnugis Along With Time')
    for i in range(len(fnus)):
        plt.plot(fnus[i].dnumber_log)

    plt.subplot(2, 3, 5)
    plt.xlabel('t/per day')
    plt.ylabel('temperature(℃)')
    plt.title('The Temperature Along With Time')
    plt.plot(temperature[:2000])

    plt.subplot(2, 3, 6)
    plt.xlabel('t/per day')
    plt.ylabel('Humidity')
    plt.title('The Humidity Along With Time')
    plt.plot(Humidity[:2000])
    plt.show()

    # plt.xlabel('extension_rate')
    # plt.ylabel('decomposition')
    # plt.title('The Decomposition Along With Extension_rate')
    # plt.plot(extension_rate, decomposition)
    # plt.show()
    return


def compare(record):
    cities = ['Manaus', 'Los Angeles.csv', 'Focus.csv', 'Turpan.csv', 'Seattle.csv']
    
    plt.xlabel('t/h')
    plt.ylabel('decomposition')
    plt.title('The Decomposition Along With Time')
    l = []
    for i in range(5):
        decomposition, litter, record_x, record_y = record[i]
        L, = plt.plot(decomposition)
        l.append(L,)
    plt.legend(handles = l, labels = cities, loc = 'best')
    plt.show()
    

    plt.xlabel('t/h')
    plt.ylabel('the left of the litter')
    plt.title('The Litter Left Along With Time')
    l = []
    for i in range(5):
        decomposition, litter, record_x, record_y = record[i]
        L, = plt.plot(litter[:1000])
        l.append(L,)
        plt.plot(record_x, record_y, 'x')
        print(record_x)
    plt.legend(handles = l, labels = cities, loc = 'best')
    plt.show()


    
    return 


def record_experment_data(fs, fnus):

    print(fnus[0].Neq)
    m2 = 800000
    threshold = 400000

    temperature, Humidity = dataset.import_data(fs)

    number = []
    decomposition = []
    extension_rate = []
    litter = []

    record_x = []
    record_y = []
    # training
    for i in range(1500):
        for j in range(50):
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

    return extension_rate, number, fnus, decomposition, litter, record_x, record_y, temperature, Humidity


# 参数设计
np.set_printoptions(precision=2)
temperature_low = np.random.normal(loc=0, scale=10, size=50)
temperature_high =  np.random.normal(loc=20, scale=10, size=50)
for i in range(50):
    if temperature_high[i] < 0:
        temperature_high[i] = 3
temperature_high = temperature_low + temperature_high

width_low = np.random.normal(loc=4, scale=2, size=50) / 10
for i in range(50):
    if width_low[i] < 0:
        width_low[i] = 1e-07

width_high = np.random.normal(loc=10, scale=4, size=50) / 10 
for i in range(50):
    if temperature_high[i] < 0:
        temperature_high[i] = 0.5
width_high = width_high + width_low

extension_rate = np.random.normal(loc=50, scale=15, size=50)/100
moisture_tolerance = np.random.normal(loc=50, scale=15, size=50)
decomposition_rate = np.random.normal(loc=15, scale=5, size=50)/100

for i in range(50):
    if extension_rate[i] <= 0:
        extension_rate[i] = 0.01
    if moisture_tolerance[i] <= 0:
        moisture_tolerance[i] = 40
    if decomposition_rate[i] <= 0:
        decomposition_rate[i] =0.10


# temperature_now = temperature[0]
# width_now = Humidity[0]
temperature_now = 27
width_now = 0.25

# number_now = np.random.normal(loc=10, scale=2, size=50)
# number_now = np.around(number_now)

number_now = []
for i in range(50):
    number_now.append(np.random.randint(5, 15))

print("temperature_low", temperature_low)
print("temperature_high", temperature_high)
print("width_low", width_low)
print("width_high", width_high)
print("extension_rate", extension_rate)
print("moisture_tolerance", moisture_tolerance)
print("decomposition_rate", decomposition_rate)
print("number_now", number_now)

F = []
K = 800000
for i in range(50):
    fnu = Q1.fnugis(extension_rate[i], temperature_high[i],
                    temperature_low[i], temperature_now,
                    width_high[i], width_low[i], width_now, 0.00035, 0.015,
                    number_now[i], K, moisture_tolerance[i], decomposition_rate[i])
    F.append(fnu)

file_csv = ['Manaus.csv', 'Los Angeles.csv', 'Focus.csv', 'Turpan.csv', 'Seattle.csv']


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

