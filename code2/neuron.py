import math
import random
from collections import defaultdict
random.seed(42)

a = 1
J_eo, J_io = 0.45*a, 0.72*a
J_ee, J_ie = 0.36*a, 0.72*a
J_ei, J_ii = -0.81*a, -1.44*a
J = {"E": {"O": J_eo, "E": J_ee+J_eo, "I": J_ei},
     "I": {"O": J_io, "E": J_ie+J_io, "I": J_ii}}
time_step = 0.1
a_r_e, a_r_i, a_d_e, a_d_i = 0.001, 0.05, 1, 0.5


class Neuron:
    def __init__(self, ntype, i, available_time=0, volume=-60):
        self.type = ntype
        self.idx = i
        self.volume = volume
        self.available_time = available_time
        self.neighbors = []
        self.threshold = -50
        self.spiked = 0
        self.synaptic_e = Synaptic("E")
        self.synaptic_i = Synaptic("I")
        self.rest = -70
        self.tau = 20 if ntype == "E" else 10

    def spike(self, time):
        if self.type == "O":
            # 随机发放动作电位
            flags = [True, False]
            flag = random.choices(flags, [1, 199])[0]
            if flag is True:
                self.spiked = 1
            return 1

        if self.volume < self.threshold:
            self.spiked = 0
            return 0
        # 膜电位超过阈值，发放动作电位
        self.reset_halt(time)
        self.spiked = 1
        return 1

    def reset_halt(self, time):
        # 重置电位，并停止活动2ms
        self.volume = -60
        if self.type == "E":
            self.available_time = time + 2
        elif self.type == "I":
            self.available_time = time + 1
        # self.synaptic_e.s = 0
        # self.synaptic_i.s = 0.1

    def step(self, time):
        # 约定：先发放电位，瞬间激活突触，打开突触通道，然后通道逐渐关闭
        # 在step之前，所有突触均已检查是否发放
        # print(self.type, self.idx, time)
        if self.type == "O":
            return 0

        if self.available_time > time:
            self.synaptic_e.decay()
            self.synaptic_i.decay()
            return 0

        # 激活突触
        for nd in self.neighbors:
            if nd.spiked:
                if nd.type == "I":
                    self.synaptic_i.rise()
                else:
                    self.synaptic_e.rise()

        self.volume += (self.rest - self.volume) / self.tau * time_step
        self.volume += self.synaptic_e.s * J[self.type]["E"]
        self.volume += self.synaptic_i.s * J[self.type]["I"]

        # self.volume = min(self.volume, self.threshold)

        # 衰减突触
        self.synaptic_e.decay()
        self.synaptic_i.decay()
        # ret = self.spike(time)
        return 0

    def __str__(self):
        return "type: {}, id: {}, num_neighbors: {}, volume: {}".format(self.type, self.idx,
                                                                        len(self.neighbors), self.volume)


class Synaptic:
    def __init__(self, ntype):
        self.s = 0  # 突触通道开放程度

        if ntype == "I":
            self.a_d = a_d_i
            self.a_r = a_r_i
        else:
            self.a_d = a_d_e
            self.a_r = a_r_e

    def rise(self):
        self.s += self.a_r * (1 - self.s)

    def decay(self):
        self.s -= self.a_d * self.s * time_step


if __name__ == '__main__':
    nd = Neuron("O", 0)
    nd.step(0)

    print(nd)