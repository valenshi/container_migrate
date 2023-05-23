# -*- coding: UTF-8 -*-

import random
import numpy as np
from deap import base, creator, tools, algorithms
# 定义容器集合
D = [(dict(CPU=1, RAM=2, DISK=100), dict(CPU=0.8, RAM=1.8, DISK=80)),
     (dict(CPU=1, RAM=2, DISK=100), dict(CPU=0.8, RAM=1.8, DISK=80)),
     (dict(CPU=2, RAM=4, DISK=200), dict(CPU=1.6, RAM=3.6, DISK=160)),
     (dict(CPU=2, RAM=4, DISK=200), dict(CPU=1.6, RAM=3.6, DISK=160)),
     (dict(CPU=4, RAM=8, DISK=400), dict(CPU=3.2, RAM=7.2, DISK=320))]

# 定义服务器节点集合
Host = [(dict(CPU=10, RAM=20, DISK=1000), []),
        (dict(CPU=10, RAM=20, DISK=1000), []),
        (dict(CPU=20, RAM=40, DISK=2000), [])]

# 定义目标函数
def evaluate(individual):
    # 获取容器和迁移目标
    migrates = [(i, j) for i, j in zip(range(5), individual) if i != j]
    # 计算通信代价
    tau = sum(w * dist(src, dst) 
              for i, (src, dst) in migrates 
              for w in D[i][0].values())
    # 计算最长停机时间
    theta = max((t - s) for i, j in migrates 
                        for s, t in [(j, j + 1)] 
                        if i == j)
    # 计算总能耗
    E = [sum(((r - sum(d.values())) / r) ** 3 for d, r in D if i in j) 
         for i, j in enumerate(individual)]
    psi = sum(e * sum(h.values()) for e, h in zip(E, Host))
    return (tau, theta, psi),

# 定义距离函数
def dist(src, dst):
    return 10 * np.linalg.norm(np.subtract(src.values(), dst.values()))

# 定义适应度函数
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

# 初始化DEAP Toolbox
toolbox = base.Toolbox()
# 定义个体和种群初始化方法
toolbox.register("indices", random.sample, range(3), 3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# 定义评估函数
toolbox.register("evaluate", evaluate)
# 定义选择、交叉和变异操作
toolbox.register("select", tools.selNSGA2)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)

# 创建种群并运行NSGA-II算法
pop = toolbox.population(n=50)
algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=50)

# 在种群中输出最优解
optimal = tools.selBest(pop, k=1)[0]
print("最优解：", optimal, " 目标函数值：", evaluate(optimal)) 