"""
 @Author: Ni Qingchao
 @Email: 20210180085@fudan.edu.cn
 @FileName: demo_animation.py
 @DateTime: 2022/10/5 10:23
 @SoftWare: PyCharm
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#define canvas
fig, ax = plt.subplots()
line, = ax.plot([],[])

#get line
def line_space(B):
    x = np.linspace(0,10,100)
    return x,x+B


def update(B):
    ax.set_xlim(0,10)
    ax.set_ylim(0,20)
    x,y = line_space(B)
    line.set_data(x,y)
    return line

ani = FuncAnimation(fig, update, frames = np.linspace(0, 20, 100), interval = 50)
ani.save("move.gif", writer = 'imgemagick', fps = 10)
plt.show()