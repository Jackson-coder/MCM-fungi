import csv
import numpy as np

def import_data(fs):
    reader = csv.reader(fs)

    lines = list(reader)
    # print(lines)

    #制作数据集（训练集样本，测试集样本，训练集标签，测试集标签）
    lines = np.array((lines[1:]))
    temperature=[]
    Humidity=[]
    for i in range(len(lines)):
        temperature.append(float(lines[i][10]))
        Humidity.append(float(lines[i][6])/(float(lines[i][10])+10))
        print(Humidity[i])
    
    return temperature,Humidity


