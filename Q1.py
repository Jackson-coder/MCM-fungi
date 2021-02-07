import numpy as np
import matplotlib.pyplot as plt
import math


class fnugis:
    def __init__(self, extension_max_g, Tmax, Tmin, T_real, Wmax, Wmin, W_real, weight_b, weight_c, number, Neq, moisture_tolerance, decomposition_rate, competition):
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

    def extension_real(self):
        Tmid = (self.Tmin+self.Tmax)/2
        Wmid = (self.Wmin+self.Wmax)/2

        delta_T = 2*abs(self.T_real-Tmid)/(self.Tmax-self.Tmin)
        delta_W = 2*abs(self.W_real-Wmid)/(self.Wmax-self.Wmin)
        if delta_T > 1:
            delta_T = 1-1e-03
        if delta_W > 1:
            delta_W = 1-1e-03

        extension_gi = self.extension_max_g * \
            (self.weight_b*(1-delta_T) +
             self.weight_c*(np.log10(1+(1-delta_W))))

        # print(self.Neq,self.extension_max_g,delta_T,self.Tmax-self.Tmin,(1-delta_T), (1-delta_W), extension_gi)
        return extension_gi


def update_real_number(fnugis, m2, threshold):
    N = 0
    Q = 0
    d_num = 0

    extension_gi = []
    total_gi = 0
    total_number = 0


    for fnugi in fnugis:
        gi = fnugi.extension_real()
        extension_gi.append(gi)
        total_gi += gi
        total_number += fnugi.number


    for i in range(len(fnugis)):

        # print(fnugis[i].number / total_number)

        if fnugis[i].Neq == 800000:
            if fnugis[i].number-1 <= 0:
                fnugis[i].number = 2
            fnugis[i].Neq = m2 #* extension_gi[i] / total_gi  # + 1000

            # print(m2, fnugis[i].Neq, delta, extension_gi[i] -
            #       delta, total_gi - delta * len(fnugis))
            fnugis[i].a = math.log(fnugis[i].Neq/fnugis[i].number-1)
        else:
            fnugis[i].Neq = m2 #* extension_gi[i] / total_gi

        sigma = 0
        for z in range(50):
            if z!=i:
                sigma += fnugis[z].competition/fnugis[i].competition

        fnugis[i].number = fnugis[i].Neq / \
            (1 + math.exp(fnugis[i].a - extension_gi[i] * fnugis[i].t))  #普通模式

        # fnugis[i].number = (fnugis[i].Neq-sigma) / \
        #     (1 + math.exp(fnugis[i].a - (1-sigma/fnugis[i].Neq)*extension_gi[i] * fnugis[i].t))

        d_number = fnugis[i].Neq*extension_gi[i] * \
            math.exp(fnugis[i].a-extension_gi[i] * fnugis[i].t) / \
            (1+math.exp(fnugis[i].a-extension_gi[i] * fnugis[i].t))**2

        # d_number = fnugis[i].Neq*extension_gi[i] * (1-sigma/fnugis[i].Neq)

        fnugis[i].t = fnugis[i].t + 1

        # print(fnugis[i].Neq,extension_gi[i],fnugis[i].a,d_number)
        N += fnugis[i].number
        Q += fnugis[i].moisture_tolerance * \
            fnugis[i].decomposition_rate*fnugis[i].number
        d_num += d_number
        fnugis[i].number_log.append(fnugis[i].number)
        fnugis[i].dnumber_log.append(d_number)

    d_num /= len(fnugis)
    Q = Q/1000000
    # print('m2, Q',m2, Q)
    m2 = m2 * (1 - Q)

    if m2 < 0:
        # print(m2, Q)
        plt.plot()
        plt.show()

    flag = 0
    if m2 < threshold and threshold > 50000:
        flag = 1
        threshold /= 2

    return N, Q, m2, d_num, flag, threshold
# 总菌数
