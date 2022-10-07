import math
import random
from collections import defaultdict
random.seed(42)

J_eo, J_io = 0.45, 0.72
J_ee, J_ie = 0.36, 0.72
J_ei, J_ii = -0.81, -1.44
J = {"E": {"O": J_eo, "E": J_ee, "I": J_ei},
     "I": {"O": J_io, "E": J_ie, "I": J_ii}}
time_step = 0.1


class Neuron:
    def __init__(self, ntype, i, available_time=0, volume=-60):
        self.type = ntype
        self.idx = i
        self.volume = volume
        self.available_time = available_time
        self.neighbors = []
        self.threshold = -50
        self.train = defaultdict(int)
        self.filter = Filter(ntype)
        self.rest = -70
        self.tau = 20 if ntype == "E" else 10

    def spike(self, time):
        # 膜电位超过阈值，发放动作电位
        if self.volume < self.threshold:
            return 0
        self.reset_halt(time)
        for i in range(100):
            self.train[time+i*time_step] += self.filter.filter_func(i*time_step) * time_step
        if time-time_step in self.train:
            self.train.pop(time-time_step)
        return 1

    def reset_halt(self, time):
        # 重置电位，并停止活动2ms
        self.volume = -60
        if self.type == "E":
            self.available_time = time + 2
        elif self.type == "I":
            self.available_time = time + 1


    def step(self, time):
        # print(self.type, self.idx, time)
        if self.type == "O":
            # TODO: 随机发放动作电位
            flags = [True, False]
            flag = random.choices(flags, [1, 199])[0]
            if flag is True:
                self.volume = -50
                self.spike(time)
            return 0

        if self.available_time > time:
            return 0

        self.volume += (self.rest - self.volume) / self.tau * time_step
        for nd in self.neighbors:
            self.volume += nd.train[time] * J[self.type][nd.type]
        # self.volume = min(self.volume, self.threshold)
        ret = self.spike(time)
        return ret

    def __str__(self):
        return "type: {}, id: {}, num_neighbors: {}, volume: {}".format(self.type, self.idx,
                                                                        len(self.neighbors), self.volume)


class Filter:
    def __init__(self, ntype):
        if ntype == "I":
            self.tau_d = 4.5
        else:
            self.tau_d = 2
        self.tau_r = 0.5

    def filter_func(self, dt):
        td = self.tau_d
        tr = self.tau_r
        return (math.exp(-dt/td) - math.exp(-dt/tr)) / (td - tr)

if __name__ == '__main__':
    nd = Neuron("O", 0)
    nd.step(0)
    f = Filter("E")
    for i in range(100):
        print(i, f.filter_func(i*time_step))
    print(nd)