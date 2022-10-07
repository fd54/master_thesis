"""
 @Author: Ni Qingchao
 @Email: 20210180085@fudan.edu.cn
 @FileName: demo_multiprocessing.py
 @DateTime: 2022/10/5 0:49
 @SoftWare: PyCharm
"""
import time
from multiprocessing import Pool


def main(name, num):
    time.sleep(1/(1+num))
    print(f'{num} {name}: Hello World')


if __name__ == '__main__':
    # 创建进程池

    p = Pool()

    for i in range(10):
        p.apply_async(func=main, args=('Lovefish', i,))

    # 关闭进程池
    p.close()

    # 阻塞进程, 等待子进程执行结束
    p.join()

    print('主进程结束')
