import numpy as np
import matplotlib.pyplot as plt
import math

class fungis:
    def __init__(self, extension_max_g, Tmax, Tmin, T_real, Wmax, Wmin, W_real, weight_b, weight_c, number, Neq, moisture_tolerance, decomposition_rate, competition, symbiosis_b, symbiosis_index,parasitic_c,parasitic_index,be_parasitic_index):
        self.extension_max_g = extension_max_g
        self.Tmax = Tmax
        self.Tmin = Tmin
        self.T_real = T_real
        self.Wmax = Wmax
        self.Wmin = Wmin
        self.W_real = W_real
        self.weight_b = weight_b
        self.weight_c = weight_c
        self.number = number
        self.Neq = Neq
        self.moisture_tolerance = moisture_tolerance
        self.decomposition_rate = decomposition_rate
        self.t = 0
        self.a = 0
        self.number_log = []
        self.dnumber_log = []
        self.competition = competition
        self.symbiosis_b = symbiosis_b
        self.symbiosis_index = symbiosis_index
        self.parasitic_c=parasitic_c
        self.parasitic_index=parasitic_index
        self.be_parasitic_index=be_parasitic_index

    def extension_real(self):
        Tmid = (self.Tmin+self.Tmax)/2
        Wmid = (self.Wmin+self.Wmax)/2

        delta_T = 2*abs(self.T_real-Tmid)/(self.Tmax-self.Tmin)
        delta_W = 2*abs(self.W_real-Wmid)/(self.Wmax-self.Wmin)
        # if delta_T > 1:
        #     delta_T = 1-1e-03
        if delta_W > 1.5:
            # delta_W = 1-1e-03
            delta_W = 1.5

        extension_gi = self.extension_max_g * \
            (self.weight_b*(1-delta_T) +
             self.weight_c*(np.log10(1+(1-delta_W))))

        # print(self.Neq,self.extension_max_g,delta_T,self.Tmax-self.Tmin,(1-delta_T), (1-delta_W), extension_gi)
        return extension_gi


def update_real_number(fungis, m2, threshold):
    N = 0
    Q = 0
    d_num = 0

    extension_gi = []
    total_gi = 0
    total_number = 0

    for fungi in fungis:
        gi = fungi.extension_real()
        extension_gi.append(gi)
        total_gi += gi
        total_number += fungi.number

    for i in range(len(fungis)):

        # print(fungis[i].number / total_number)

        if fungis[i].Neq == 800000:
            if fungis[i].number-1 <= 0:
                fungis[i].number = 2
            fungis[i].Neq = m2  # * extension_gi[i] / total_gi  # + 1000

            # print(m2, fungis[i].Neq, delta, extension_gi[i] -
            #       delta, total_gi - delta * len(fungis))
            fungis[i].a = math.log(fungis[i].Neq/fungis[i].number-1)
        else:
            fungis[i].Neq = m2  # * extension_gi[i] / total_gi

        sigma = 0
        for z in range(len(fungis)):
            if z != i:
                sigma += fungis[z].competition / \
                    fungis[i].competition*fungis[z].number

        # 普通模式
        # fungis[i].number = fungis[i].Neq / \
        #     (1 + math.exp(fungis[i].a - extension_gi[i] * fungis[i].t))

        # if fungis[i].number < 0:
        #     fungis[i].number = 0

        # d_number = fungis[i].Neq*extension_gi[i] * \
        # math.exp(fungis[i].a-extension_gi[i] * fungis[i].t) / \
        #     (1+math.exp(fungis[i].a-extension_gi[i] * fungis[i].t))**2

        # 竞争模式
        fungis[i].number = (fungis[i].Neq-sigma) / \
            (1 + math.exp(fungis[i].a - (1-sigma/fungis[i].Neq)*extension_gi[i] * fungis[i].t)) #竞争模式

        if fungis[i].number < 0:
            fungis[i].number = 0

        d_number = extension_gi[i] * (1-sigma/fungis[i].Neq)*fungis[i].number

        #竞争模式 + 共生模式
        # gamma = 0
        # if fungis[i].symbiosis_index != 0:
        #     gamma = fungis[i].symbiosis_b*fungis[int(fungis[i].symbiosis_index)].number
        
        # fungis[i].number = (fungis[i].Neq-sigma+gamma) / \
        #     (1 + math.exp(fungis[i].a - (1-sigma /
        #                                  fungis[i].Neq+gamma)*extension_gi[i] * fungis[i].t))

        # if fungis[i].number < 0:
        #     fungis[i].number = 0

        # d_number = extension_gi[i] * (1-sigma/fungis[i].Neq+gamma/fungis[i].Neq)*fungis[i].number

        #竞争模式 + 共生模式 + 寄生模式 
        # gamma = 0
        # belta = 0
        # alpha = 0
        # d_number = 0
        # if fungis[i].symbiosis_index != 0:
        #     gamma = fungis[i].symbiosis_b*fungis[int(fungis[i].symbiosis_index)].number
        # if fungis[i].parasitic_index != 0:
        #     belta = 1
        # if fungis[i].be_parasitic_index != 0:
        #     alpha = 1
            
        
    
        # if fungis[i].number < 0:
        #     fungis[i].number = 0

        # if alpha == 1:
        #     d_number = extension_gi[i] * (1-sigma/fungis[i].Neq-gamma/fungis[i].Neq)*fungis[i].number
        #     fungis[i].number = (fungis[i].Neq-sigma-gamma) / (1 + math.exp(fungis[i].a - (1-sigma /fungis[i].Neq-gamma/fungis[i].Neq)*extension_gi[i] * fungis[i].t))
        # if belta == 1:
        #     fungis[i].number = fungis[i].Neq*(-fungis[i].parasitic_c/extension_gi[i]+gamma-sigma) / \
        #     (1 + math.exp(fungis[i].a - (-fungis[i].parasitic_c+extension_gi[i]*(gamma-sigma))))
        #     d_number = (-fungis[i].parasitic_c+extension_gi[i]*(gamma-sigma))*fungis[i].number


        fungis[i].t = fungis[i].t + 1

        # print(fungis[i].Neq, extension_gi[i],m2,
        #       fungis[i].a, d_number, fungis[i].number)
        N += fungis[i].number
        Q += fungis[i].moisture_tolerance * \
            fungis[i].decomposition_rate*fungis[i].number
        d_num += d_number
        fungis[i].number_log.append(fungis[i].number)
        fungis[i].dnumber_log.append(d_number)

    d_num /= len(fungis)
    Q = Q/1000000
    # print('m2, Q',m2, Q)
    m2 = m2 * (1 - Q)

    if m2 < 0:
        print(m2, Q)
        plt.plot()
        plt.show()

    flag = 0
    if m2 < threshold and threshold > 50000:
        flag = 1
        threshold /= 2

    return N, Q, m2, d_num, flag, threshold
# 总菌数
