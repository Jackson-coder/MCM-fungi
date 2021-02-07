import numpy as np
import matplotlib.pyplot as plt
import dataset
import Q1
import copy


def draw(extension_rate, number, fnus, decomposition, temperature, Humidity):
    plt.subplot(2, 3, 1)
    plt.xlabel('t/day')
    plt.ylabel('extension rate')
    plt.title('The Extension Rate Along With Time')
    plt.plot(extension_rate)

    plt.subplot(2, 3, 2)
    plt.xlabel('t/day')
    plt.ylabel('amount of fungi')
    plt.title('The Amount of Whole Fungi Along With Time')
    plt.plot(number)

    plt.subplot(2, 3, 3)
    plt.xlabel('t/day')
    plt.ylabel('amount of fungi')
    plt.title('The Amount of ALl Fungi Along With Time')
    for i in range(len(fnus)):
        plt.plot(fnus[i].number_log)

    plt.subplot(2, 3, 4)
    plt.xlabel('t/day')
    plt.ylabel('acceleration of fungi growth')
    plt.title('The Acceleration of ALl fungi Along With Time')
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
    for i in range(5):
        decomposition, litter, record_x, record_y = record[i]
        L, = plt.plot(decomposition)
        l.append(L,)
    plt.legend(handles=l, labels=cities, loc='best')
    plt.show()

    plt.xlabel('t/day')
    plt.ylabel('the left of the woody fibers')
    plt.title('The Woody Fibers Left Along With Time')
    l = []
    for i in range(5):
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

    number = []
    decomposition = []
    extension_rate = []
    litter = []

    record_x = []
    record_y = []
    # training
    for i in range(5000):
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
        # plt.plot()
        # plt.show()
    return extension_rate, number, fnus, decomposition, litter, record_x, record_y, temperature, Humidity


# 参数设计
np.set_printoptions(precision=2)
temperature_low = np.random.normal(loc=0, scale=10, size=50)
temperature_high = np.random.normal(loc=20, scale=10, size=50)
for i in range(50):
    if temperature_high[i] < 0:
        temperature_high[i] = 3
temperature_high = temperature_low + temperature_high

temperature = (temperature_high + temperature_low) / 2

width_low = np.random.normal(loc=4, scale=2, size=50) / 10
for i in range(50):
    if width_low[i] < 0:
        width_low[i] = 1e-07

width_high = np.random.normal(loc=10, scale=4, size=50) / 10
for i in range(50):
    if temperature_high[i] < 0:
        temperature_high[i] = 0.5
width_high = width_high + width_low

width = (width_high + width_low) / 2

extension_rate = np.random.normal(loc=50, scale=15, size=50)/100
moisture_tolerance = np.random.normal(loc=50, scale=15, size=50)
decomposition_rate = np.random.normal(loc=15, scale=5, size=50)/100

# 定义竞争因子
competition_a = np.random.normal(loc=50, scale=15, size=50)/100

# 定义共生因子
flag = 0
symbiosis_b = np.zeros(50)
symbiosis_index = np.zeros(50)

# 定义寄生因子
f_flag = 0
parasitic_c = np.zeros(50)
parasitic_index = np.zeros(50)


for i in range(50):
    for j in range(50):
        if i != j and i!=0 and j!=0 and abs(temperature[i]-temperature[j]) < 5 and abs(width[i] - width[j]) < 0.4:
            flag += 1
            symbiosis_b[i] = 0.2
            symbiosis_index[i] = j
            symbiosis_b[j] = 0.1
            symbiosis_index[j] = i
            if flag == 2:
                break
    if flag == 2:
        break


for i in range(25):
    for j in range(25):
        if i != j and abs(temperature[25+i]-temperature[25+j]) < 5 and abs(width[25+i] - width[25+j]) < 0.4:
            f_flag += 1
            parasitic_c[25+i] = 1
            parasitic_index[25+i] = 25+j
            parasitic_index[25+j] = i
            break
    if f_flag == 1:
        break


for i in range(50):
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
    fnu = Q1.fungis(extension_rate[i], temperature_high[i],
                    temperature_low[i], temperature_now,
                    width_high[i], width_low[i], width_now, 0.00035, 0.015,
                    number_now[i], K, moisture_tolerance[i], decomposition_rate[i], competition_a[i], symbiosis_b[i], symbiosis_index[i],parasitic_c[i],parasitic_index[i])
    F.append(fnu)

file_csv = ['Manaus.csv', 'Los Angeles.csv',
            'Focus.csv', 'Turpan.csv', 'Seattle.csv']


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
