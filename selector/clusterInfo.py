# 只负责统计集群相关信息，不提供检查，因为还需要分为Pod与VM呢
# 提供节点列表、功耗限制的字典、能耗价格的字典、cpu与内存使用率的字典、触发因子
# 在创建的时候就通过读取文件来进行初始化，如果初始化失败就会报错
# 额外实现的函数来进行迁移触发
import configparser
import os
import sys
# 老师，那我就这个月中旬左右去深圳实习了，然后转正答辩之后再回来，可以吗
home_dir = os.path.expanduser("~")
sys.path.append(home_dir+'/container_migrate/utils')
from mysqltool import MySQLTool

conf_url = os.path.expanduser("~/datacenter_energy/config/dataserv.conf")



def readConf(para):
    try:
        # 读取 dataserv.conf 文件
        conf = configparser.ConfigParser()
        conf.read(conf_url)
        # 获取 [para] 部分的列表项
        result = conf.items(para)
        return dict(result)
    except:
        print("Error: Failed to load dataserv.conf file")

class Host:
    # 单台主机的信息
    # 提供单台主机的行为
    # 定义行为与信息
    def __init__(self, host_name):
        # 列表类型,存放此主机上的Pod集合
        self.pod_list = []



        # 主机名称，字符串类型
        self.host_name = host_name
        # 节点ip，字符串类型
        self.ip = ""
        # 节点状态：分为可用与不可用多种状态：关机、正常、开机但不可用、休眠中、未知
        self.host_status = "unkown"
        # 功耗限制，为浮点类型
        self.power_limit = 0.0
        # 能耗价格，浮点类型
        self.energy_cost = 0.0
        # 节点功耗,浮点数
        self.power = 0.0
        # cpu最近时刻的负载百分比，浮点类型
        self.cpu_load = 0.0
        # 内存最近时刻的负载，浮点类型
        self.mem_load = 0.0
        # cpu超限次数，整数类型
        self.cpu_record = 0
        # 内存超限次数，整数类型
        self.mem_record = 0
        # 功耗超限次数，整数类型
        self.power_record = 0
        # 载入基本信息
        self.reload()

        # 如何记录超限的信息呢?通过十个大小的数组,使用循环指针赋值,每次超限了就赋值为1,数组之和就是超限次数
        self.rd = []
        self.rd.append([])
        self.rd.append([])
        self.rd.append([])

    # 更新操作
    def update(self):
        # 就剩status了
        # status不更新也行, 可以手动操作
        # update最好每隔4s或者10s调用一次
        # 需要更新 power, cpu_load、mem_load、cpu_record mem_record power_record
        db_tool = MySQLTool(host='192.168.1.201', username='ecm', password='123456', database='ecm')
        result = db_tool.select('latest_nodedata', columns=['*'], where="node_name='"+self.host_name + "'")
        db_tool.close()

        dict = result[0]
        self.power = float(dict['power'])
        self.cpu_load = float(dict['cpu_load'])
        self.mem_load = float(dict['memory_load'])
        
        # 更新记录数组
        if self.power > self.power_limit*0.8:
            self.rd[0].append(1)
        else:
            self.rd[0].append(0)
        # 暂时设置利用率上限为75%
        if self.cpu_load > 75:
            self.rd[1].append(1)
        else:
            self.rd[1].append(0)
        
        if self.mem_load > 75:
            self.rd[2].append(1)
        else:
            self.rd[2].append(0)
        
        # 更新record
        if len(self.rd[0]) > 1:
            self.power_record -= self.rd[0][0]
            self.rd[0].pop(0)
        self.power_record += self.rd[0][-1]
        

        if len(self.rd[1]) > 1:
            self.cpu_record -= self.rd[1][0]
            self.rd[1].pop(0)
        self.cpu_record += self.rd[1][-1]
        

        if len(self.rd[2]) > 1:
            self.mem_record -= self.rd[2][0]
            self.rd[2].pop(0)
        self.mem_record += self.rd[2][-1]

        

    # 从文件载入基本信息操作, 频率可能不高
    def reload(self):
        # 从conf读取主机列表、功耗限制、能耗价格
        self.ip = readConf("hosts")[self.host_name]
        self.power_limit = float(readConf("powerLimit")[self.host_name])
        self.energy_cost = float(readConf("energyCost")[self.host_name])

    # 打印相关信息操作
    def getInfo(self):
        ret = {}
        ret['host_name'] = self.host_name
        ret['ip'] = self.ip
        ret['power_limit'] = self.power_limit
        ret['energy_cost'] = self.energy_cost
        ret['host_status'] = self.host_status
        ret['power'] = self.power
        ret['cpu_load'] = self.cpu_load
        ret['mem_load'] = self.mem_load
        ret['cpu_record'] = self.cpu_record
        ret['mem_record'] = self.mem_record
        ret['power_record'] = self.power_record
        return ret
    
    

# 使用流程:
# 在新建好实例之后, 周期性的调用update即可
class Cluster:
    # 集群信息，包含多个主机，提供管理主机集合的操作
    # 定义行为与信息
    # 主机列表，包含所有主机
    def __init__(self):
        self.host_list = []

        for it in readConf("hosts").items():
            self.addHost(it[0]) # it[0]为主机名
            # print(it[0])

    # 添加一个host到hostList中
    def addHost(self, host):
        # 是否需要做合法性检验？
        self.host_list.append(Host(host))

    # 更新主机列表
    def update(self):
        # 要对列表进行筛选，删去不合法的主机列表
        for host in self.host_list:
            host.update()

# cluster = Cluster()
# for host in cluster.host_list:
#     host.update()
#     host.getInfo()