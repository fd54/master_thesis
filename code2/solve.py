"""
 @Author: Ni Qingchao
 @Email: 20210180085@fudan.edu.cn
 @FileName: solve.py
 @DateTime: 2022/10/5 20:49
 @SoftWare: PyCharm
"""
import os
import sys
import pickle
import random
import time
from multiprocessing import Process, Pool
from tqdm import tqdm
from matplotlib import pyplot as plt
from matplotlib import animation
from neuron import Neuron

sys.setrecursionlimit(2 ** 31 - 1)
N_o = N_e = 800
N_i = 200
p = 0.2
time_step = 0.1

if not os.path.exists("neurons.pkl"):
    neuron_o = [Neuron("O", i, available_time=-1) for i in range(N_o)]
    neuron_e = [Neuron("E", i) for i in range(N_e)]
    neuron_i = [Neuron("I", i) for i in range(N_i)]
    neuron_all = neuron_o + neuron_e + neuron_i
    neuron_all[0].neighbors.append(neuron_all[1])
    neuron_all[1].neighbors.append(neuron_all[0])

    for nd1 in tqdm(neuron_all):
        for nd2 in neuron_all:
            if nd1 == nd2:
                continue
            conn_w = random.randint(1, 5)
            if conn_w == 1:
                nd1.neighbors.append(nd2)
    # with open("./neurons.pkl", "wb") as f:
    #     print("dumping")
    #     pickle.dump(neuron_all, f)
    #     print("dumped")

else:
    with open("./neurons.pkl", "rb") as f:
        neuron_all = pickle.load(f)
        neuron_e = neuron_all[N_o: N_e + N_o]
        neuron_i = neuron_all[-N_i:]
        assert all([nd.type == "E" for nd in neuron_e])
        assert all([nd.type == "I" for nd in neuron_i])

        # print(neuron_all[0])


def ode():
    v_e = []
    v_i = []

    f = open("result{}.txt".format(int(time.time()) % 1000), "a+")
    num_step = 800
    firing_rate_e = [0] * num_step
    firing_rate_i = [0] * num_step
    synaptic_rate_e = [0] * num_step
    synaptic_rate_i = [0] * num_step

    for i in tqdm(range(num_step)):
        t = i * time_step

        cnt_e, cnt_i = 0, 0
        for neuron in neuron_all:
            neuron.spike(t)
            if neuron.type == "E":
                cnt_e += neuron.spiked
            elif neuron.type == "I":
                cnt_i += neuron.spiked

        for neuron in neuron_all:
            neuron.step(t)
        synaptic_rate_e[i] = neuron.synaptic_e.s
        synaptic_rate_i[i] = neuron.synaptic_i.s
        ve_cur, vi_cur = calc(neuron_e), calc(neuron_i)
        firing_rate_e[i] = cnt_e
        firing_rate_i[i] = cnt_i
        v_e.append(ve_cur)
        v_i.append(vi_cur)
        f.write("{:.5f}\t{:.5f}\n".format(ve_cur, vi_cur))

    f.close()
    plt.subplot(221)
    plt.plot(firing_rate_e, "g")
    plt.plot(firing_rate_i, "r")
    plt.subplot(222)
    plt.plot(synaptic_rate_e, "g")
    plt.plot(synaptic_rate_i, "r")
    plt.subplot(223)
    plt.plot(v_e, "g")
    plt.plot(v_i, "r")
    plt.show()


def calc(neurons):
    return sum([nd.volume for nd in neurons]) / len(neurons)


if __name__ == '__main__':
    ode()
