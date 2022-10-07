"""
 @Author: Ni Qingchao
 @Email: 20210180085@fudan.edu.cn
 @FileName: demo_time.py
 @DateTime: 2022/10/5 14:32
 @SoftWare: PyCharm
"""
import time
import math
from functools import lru_cache

@lru_cache(None)
def calc(x):
    return math.exp(x)

t1 = time.time()
for i in range(10000000):
    math.exp(0.01)
print(time.time()-t1)

t1 = time.time()
for i in range(10000000):
    calc(0.01)
print(time.time()-t1)
if __name__ == '__main__':
    pass
