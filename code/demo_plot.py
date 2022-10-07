"""
 @Author: Ni Qingchao
 @Email: 20210180085@fudan.edu.cn
 @FileName: demo_plot.py
 @DateTime: 2022/10/5 10:49
 @SoftWare: PyCharm
"""
from matplotlib import pyplot as plt

result_file = "result345.txt"
with open(result_file) as f:
    data = [item.strip().split('\t') for item in f.readlines()]
v_e = [float(i) for i, _ in data]
v_i = [float(j) for _, j in data]
plt.plot(v_e, "g")
plt.plot(v_i, "r")
plt.show()
if __name__ == '__main__':
    pass
