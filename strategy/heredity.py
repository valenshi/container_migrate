import random

# 定义目标函数1
def objective_function_1(x):
    return x**2

# 定义目标函数2
def objective_function_2(x):
    return (x-2)**2

# 定义种群类
class Population:
    def __init__(self, size):
        self.individuals = []
        for i in range(size):
            self.individuals.append(Individual())

# 定义个体类
class Individual:
    def __init__(self):
        self.x = random.uniform(-5, 5)
        self.fitnesses = [objective_function_1(self.x), objective_function_2(self.x)]

    # 计算个体适应度
    def calculate_fitness(self):
        self.fitnesses = [objective_function_1(self.x), objective_function_2(self.x)]

# 定义遗传算法类
class GeneticAlgorithm:
    def __init__(self, pop_size, num_generations, crossover_rate, mutation_rate):
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = Population(pop_size)

    # 计算种群中所有个体的适应度
    def calculate_fitness_of_population(self):
        for individual in self.population.individuals:
            individual.calculate_fitness()

    # 选择个体进行繁殖
    def selection(self):
        parents = []
        # 轮盘赌选择
        total_fitness = sum([sum(individual.fitnesses) for individual in self.population.individuals])
        for i in range(2):
            pick = random.uniform(0, total_fitness)
            current = 0
            for individual in self.population.individuals:
                current += sum(individual.fitnesses)
                if current > pick:
                    parents.append(individual)
                    break
        return parents

    # 进行交叉操作
    def crossover(self, parents):
        if random.uniform(0, 1) < self.crossover_rate:
            # 简单随机交叉
            child1_x = random.uniform(min(parents[0].x, parents[1].x), max(parents[0].x, parents[1].x))
            child2_x = random.uniform(min(parents[0].x, parents[1].x), max(parents[0].x, parents[1].x))
        else:
            child1_x = parents[0].x
            child2_x = parents[1].x
        child1 = Individual()
        child1.x = child1_x
        child2 = Individual()
        child2.x = child2_x
        return [child1, child2]

    # 进行变异操作
    def mutation(self, child):
        if random.uniform(0, 1) < self.mutation_rate:
            # 简单变异
            child.x = random.uniform(-5, 5)
        return child

    # 进化
    def evolve(self):
        for generation in range(self.num_generations):
            print("Generation ", generation+1)
            self.calculate_fitness_of_population()
            print("Best fitnesses of generation: ", [min(individual.fitnesses) for individual in self.population.individuals])
            new_population = Population(self.pop_size)
            for i in range(int(self.pop_size/2)):
                parents = self.selection()
                children = self.crossover(parents)
                children[0] = self.mutation(children[0])
                children[1] = self.mutation(children[1])
                new_population.individuals[i*2] = children[0]
                new_population.individuals[i*2+1] = children[1]
            self.population = new_population
        self.calculate_fitness_of_population()
        return min(self.population.individuals, key=lambda individual: sum(individual.fitnesses)).x

# 运行遗传算法
genetic_algorithm = GeneticAlgorithm(pop_size=50, num_generations=20, crossover_rate=0.8, mutation_rate=0.1)
x_optimal = genetic_algorithm.evolve()
print("Optimal x: ", x_optimal)
print("Objective function 1 of optimal x: ", objective_function_1(x_optimal))
print("Objective function 2 of optimal x: ", objective_function_2(x_optimal))

# 如果面对不同的目标函数，上述代码需要修改以下部分：
# 定义新的目标函数，替换原有的目标函数1和目标函数2。
# 在Individual类中的calculate_fitness函数中，计算新的目标函数的适应度。
# 改变遗传算法类的实例化时传入的参数，包括目标函数的个数和计算适应度时需要用到的目标函数。