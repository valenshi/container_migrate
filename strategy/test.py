import random
from functools import cmp_to_key

# 定义多目标函数
def fitness_function(individual):
    x, y = individual[0], individual[1]
    f1 = x**2 + y**2
    f2 = (x - 2)**2 + (y - 1)**2
    return [f1, f2]

# 个体编码
def individual(min_val, max_val):
    return [random.uniform(min_val, max_val) for _ in range(2)]

# 初始化种群
def population(pop_size, min_val, max_val):
    return [individual(min_val, max_val) for _ in range(pop_size)]

# 计算适应度
def fitness(individual):
    return fitness_function(individual)

# 非支配排序
def non_dominated_sort(population):
    fronts = []
    pop_size = len(population)
    # 初始化每个个体的被支配的次数
    dom_count = [0] * pop_size
    # 初始化每个个体的支配对象集合
    dominate_set = [[] for _ in range(pop_size)]
    # 初始化每个个体的非支配集合
    non_dom_set = [[]]
    # 遍历种群中的每个个体
    for i in range(pop_size):
        # 用于存储当前个体支配的个体
        s = []
        # 用于存储当前个体被支配的次数
        n = 0
        for j in range(pop_size):
            if i == j:
                continue
            # 检查个体 i 是否支配个体 j
            if all([fitness_function(i)[k] <= fitness_function(j)[k] for k in range(2)]):
                s.append(j)
            # 检查个体 i 是否被个体 j 支配
            elif all([fitness_function(i)[k] >= fitness_function(j)[k] for k in range(2)]):
                n += 1
        # 记录被当前个体支配的对象集合和被支配次数
        dominate_set[i] = s
        dom_count[i] = n
        # 如果当前个体是非支配的，则添加到非支配集合中
        if n == 0:
            non_dom_set[0].append(i)
    # 分层，按照被支配次数从小到大进行排序
    i = 0
    while non_dom_set[i]:
        temp = []
        for a in non_dom_set[i]:
            for b in dominate_set[a]:
                dom_count[b] -= 1
                if dom_count[b] == 0:
                    temp.append(b)
        i += 1
        non_dom_set.append(temp)
    # 将种群按照非支配层数进行排序
    for f, front in enumerate(non_dom_set):
        fronts += [(f+1, i) for i in front]
    return fronts

# 计算每个个体的距离
def crowding_distance(front):
    n = len(front)
    for i in range(n):
        front[i].append(0)
    for i in range(2):
        front.sort(key=lambda x: x[i])
        front[0][2] = float('inf')
        front[-1][2] = float('inf')
        for j in range(1, n-1):
            front[j][2] += (front[j+1][i] - front[j-1][i]) / (front[-1][i] - front[0][i])
    for i in range(n):
        front[i].pop()
    return front

# 个体选择
def selection(fronts):
    new_pop = []
    pop_size = 0
    # 从第一层开始，直到选择的个体数量达到种群大小
    n = 0
    while pop_size < 100:
        if pop_size + len(fronts[n]) > 100:
            break
        for i in fronts[n]:
            new_pop.append(i)
        pop_size += len(fronts[n])
        n += 1
    # 如果还未达到种群数量，则按照距离排序，选择离当前解最近的个体
    if pop_size < 100:
        fronts[n] = crowding_distance(fronts[n])
        fronts[n].sort(key=lambda x: x[2], reverse=True)
        for i in range(100 - pop_size):
            new_pop.append(fronts[n][i])
    return new_pop

# 基因交叉
def crossover(parent1, parent2):
    a = random.random()
    child1 = [a * parent1[i] + (1 - a) * parent2[i] for i in range(len(parent1))]
    child2 = [(1 - a) * parent1[i] + a * parent2[i] for i in range(len(parent2))]
    return [child1, child2]

# 基因变异
def mutation(individual, min_val, max_val):
    for i in range(len(individual)):
        if random.random() < 0.1:
            individual[i] = random.uniform(min_val, max_val)
    return individual

# 遗传算法主体
def genetic_algorithm(pop_size, min_val, max_val, num_generations):
    # 初始化种群
    pop = population(pop_size, min_val, max_val)