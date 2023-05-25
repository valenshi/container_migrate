# 只负责统计集群相关信息，不提供检查，因为还需要分为Pod与VM呢
# 提供节点列表、功耗限制的字典、能耗价格的字典、cpu与内存使用率的字典、触发因子
# 在创建的时候就通过读取文件来进行初始化，如果初始化失败就会报错
# 额外实现的函数来进行迁移触发
import configparser
import os
import sys

home_dir = os.path.expanduser("~")
sys.path.append(home_dir, '/container_migrate/utils', 'mysqltool.py')
from utils.mysqltool import MySQLTool

conf_url = os.path.expanduser("~/datacenter_energy/config/dataserv.conf")

class clusterInfo:
    def __init__(self):
        # 节点列表，字典类型
        self.hostlist = {}
        # 节点状态：分为可用与不可用多种状态：关机、正常、开机但不可用、休眠中、未知
        self.hostStatus = {}
        # 迁移队列，需要迁移的pod列表或者虚拟机列表，为字符串列表, 为pod名称列表
        self.powerLimit = {}
        # 能耗价格，字典类型
        self.energyCost = {}
        # cpu最近时刻的负载，字典类型
        self.cpuLoad = {}
        # 内存最近时刻的负载，字典类型
        self.memLoad = {}
        # cpu超限次数，字典类型
        self.cpuRecord = {}
        # 内存超限次数，字典类型
        self.memRecord = {}
        # 功耗超限次数，字典类型
        self.powerRecord = {}

        # 在这儿实现载入逻辑
        # 从conf读取主机列表、功耗限制、能耗价格
        self.hostlist = self.readConf("hosts")
        self.powerLimit = self.readConf("powerLimit")
        self.energyCost = self.readConf("energyCost")

        # 初始化超限记录
        for key,value in self.hostlist.items():
            self.cpuRecord[key] = 0
            self.memRecord[key] = 0
            self.powerRecord[key] = 0
            self.hostStatus[key] = self.getStatus(key, value)
        # 需要更新 hostStatus
        db_tool = MySQLTool(host='192.168.1.201', username='ecm', password='123456', database='ecm')
        db_tool.close()
        
    def getStatus(self, hostName, ip):
        # 更新方法？通过api的ping判断？
        # 到底如何获取、存储状态？种植运行之后又如何做？通过文件吗？
        # hostname , status, timestamp, 
        # -1 表示未知， 0 表示down，1 表示正常，2 表示uncornd
        status = -1
        
        return status

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
        print("host: ", self.hostlist)
        print("energyCost: ", self.energyCost)
        print("powerLimit: ", self.powerLimit)

        print("cpuRecord: ", self.cpuRecord)
        print("memRecord: ", self.memRecord)
        print("powerRecord: ", self.powerRecord)
        print("hostStatus: ", self.hostStatus)
        return
    
    def readConf(self, para):
        try:
            # 读取 dataserv.conf 文件
            conf = configparser.ConfigParser()
            conf.read(conf_url)
            # 获取 [para] 部分的列表项
            result = conf.items(para)
            return dict(result)
        except:
            print("Error: Failed to load dataserv.conf file")


c = clusterInfo()
c.getInfo()

# 这里需要不需要用单台主机的方法呢? 最好还是不要, 因为这样会增加工作量, 主机列表信息都是可以统一读取的, 而pod则需要单独考虑
# 所有这里只需要发出迁移命令, 给出迁移列表, 需要禁用的主机列表就可以了, 迁移、禁用、解禁都由 apiserver 完成
