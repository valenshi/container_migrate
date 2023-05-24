# 只负责统计集群相关信息，不提供检查，因为还需要分为Pod与VM呢
# 提供节点列表、功耗限制的字典、能耗价格的字典、cpu与内存使用率的字典、触发因子
# 在创建的时候就通过读取文件来进行初始化，如果初始化失败就会报错
# 额外实现的函数来进行迁移触发

class clusterInfo:
    def __init__(self):
        # 节点列表，字典类型
        self.nodelist = []
        # 迁移队列，需要迁移的pod列表或者虚拟机列表，为字符串列表
        self.migrateQueue = []
        # 功耗限制，字典类型
        self.powerLimit = []
        # 能耗价格，字典类型
        self.energyCost = []
        # cpu最近时刻的负载，字典类型
        self.cpuLoad = []
        # 内存最近时刻的负载，字典类型
        self.memLoad = []
        # cpu超限次数，字典类型
        self.cpuRecord = []
        # 内存超限次数，字典类型
        self.memRecord = []
        # 功耗超限次数，字典类型
        self.powerRecord = []


    def update(self):
    # 通过读取实时数据，更新相关信息，更新触发因子
    # 如果某些限制型信息更新了，那么要重新统计
        return

    def reload(self):
    # 重新初始化，即重新从文件读取数据
        self.__init__(self)
        return

    def getInfo(self):
    # 输出相关信息，调试用
        return
    
    