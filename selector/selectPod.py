# 最终输出的是一个列表，即migrateQueue
# 同时要负责锁定某些主机，并保存锁定列表，在迁移完成之后解除锁定
# 周期性扫描？
# 维护信息列表
# 周期性测试是否满足触发条件
import os
import sys
import time
import pymysql

home_dir = os.path.expanduser("~")
sys.path.append(home_dir+'/container_migrate/migrate')
import apiserver as mAPI
sys.path.append(home_dir+'/container_migrate/utils')
from mysqltool import MySQLTool

from clusterInfo import Cluster
from podInfo import podInfo
migrateQueue = [] # 迁移队列, 字符串列表
banHost = [] # 需要禁用的主机列表
sleepHost = [] # 需要进入睡眠状态的主机列表


def selectPodfromHost(host):
    # host: Host类型实例
    # 从host主机上筛选出需要迁出的pod列表并返回即可
    mpod_list = [] # 存放Pod类型需要迁出的实例集合
    pod_list = sorted(host.pod_list) # 此处已经重载了pod类型的比较函数, 这里按照功耗降序
    res_power = host.power

    # 将超出功耗的部分迁出
    while res_power > host.power_limit*0.8:
        mpod_list.append(pod_list[0])
        res_power -= pod_list[0].power
        pod_list.pop(0)
    
    return mpod_list

# 返回mhost_list,为迁出主机集
def checkPowerLimit(host_list):
    # pod_list 是字典类型, key为主机名, value 为 podInfo 类型的列表
    # cluster_info 为 clusterInfo 类的实例

    # 检查功耗超限次数是否达到阈值, 如果是则标记该主机, 并且将其中部分pod迁出
    mhost_list = [] #主机列表,存放Host类型实例

    for host in host_list:
        if host.power_record >= 0: # 设置超限次数
            mhost_list.append(host)
        
    # # 此时mhost_list是需要迁出的主机列表, 同时也是需要禁用的主机列表

    return mhost_list


def migratePod(mpod_list, mhost_list):
    # mpod_list: 迁出pod集
    # mhost_list: 迁出主机集

    # 实现迁移逻辑
    # 首先标记禁止迁入迁出的主机
    # 接着触发被动迁移
    # 最后解除主机标记
    # 问题在于如何获取迁移状态, 即迁移是否完成 ? 单线程同步
    # 还需要统计每个pod的状态!!!

    # 调用迁移接口
    if len(mpod_list) == 0 or len(mhost_list) == 0:
        return
    
    # 开始迁移
    # 禁用主机调度(防止调度回源主机)
    for host in mhost_list:
        mAPI.banHost(host.host_name)
    
    # 调出pod
    for pod in mpod_list:
        result = mAPI.migratePod(pod.pod_name) # 阻塞,未完成不许返回!
        if(result == "Failed"):
            # 打印日志!
            break
        print(pod.pod_name + " had migrated from " + pod.host_name + "to " + result + "! ")
        
    #解禁主机
    for host in mhost_list:
        mAPI.unbanHost(host.host_name)
    
    # 异常处理与日志输出?
    return

def getPodFromHost(host_name):
    # 通过mysql来获得host_name上的所有pod信息，这些信息都是podInfo类型的
    # print(host_name, ip)
    pod_list = []
    # 从数据库中获取也是可以的
    db_tool = MySQLTool(host='192.168.1.201', username='ecm', password='123456', database='ecm')
    # 还是需要做限制的，要去除过期数据
    # 这里还有一个视图，为 latest_poddata，针对每个pod仅显示一次
    # ALTER TABLE latest_poddata CHANGE node_name ip 
    result = db_tool.select('latest_poddata', columns=['*'], where="node_name='"+host_name + "'")
    for dict in result:
        # print(dict)
        pod = podInfo()
        pod.pod_name = dict['pod_name']
        pod.host_name = host_name
        pod.cpu_load = dict['cpu_load']
        pod.mem_load = dict['memory_load']
        # pod.status = mAPI.getPodStatus(pod.pod_name)
        pod.updata() # 更新获取status和host_name
        pod.power = mAPI.predictPower(pod.cpu_load, pod.mem_load)
        if(pod.status != "Overdue"):
            pod_list.append(pod)
    # 需要更新power与status
    db_tool.close()
    return pod_list

def getPodList(host_list):
    # 获取host_list中全部的pod,一般用于关闭主机时选择全部pod
    # 从哪儿获得数据呢？从api
    pod_list = []
    
    for host in host_list:
        host.pod_list = getPodFromHost(host.host_name)
        pod_list += host.pod_list
    return pod_list

def run():
    # 用于实现迁移触发流程，循环检查是否满足触发条件
    cluster = Cluster()
    # pod_list = getPodList(cluster.host_list)

    while True:
        cluster.update() #周期性调用update, 更新record
        pod_list = getPodList(cluster.host_list) # 更新每个host的podlist
        mhost_list = checkPowerLimit(cluster.host_list) # 找出功耗超限的主机列表
        mpod_list = []
        for host in mhost_list:
            mpod_list += selectPodfromHost(host)

        migratePod(mpod_list, mhost_list)

        time.sleep(10)

# 单线程执行
run()