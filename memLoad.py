# 该脚本负责占用一定大小的内存，并频繁读写，用来模仿IO密集型应用
# 首先设置全局变量

import os

# 设置共使用内存大小

os.environ["MALLOC_ARENA_MAX"] = "2"

# 定义频繁读写内存的函数


def memLoad(size):
    for i in range(size):
        a = [1] * 100000000

    # 频繁的读写数据，随机IO

    for i in range(size):
        a[i] = i
    
    

    # 占用内存一定时间之后释放掉
    del a

    return