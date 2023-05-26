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

from clusterInfo import clusterInfo
from podInfo import podInfo
migrateQueue = [] # 迁移队列, 字符串列表

def selectPodfromHost(pod_set, hostname):
    # pod_set: 某台主机上的 podInfo 类的列表
    # hostname: 主机名称
    # 从 hostname 主机上筛选出可以迁出的pod列表
    
    pass

def checkPowerLimit(pod_list, cluser_info):
    # pod_list 是字典类型, key为主机名, value 为 podInfo 类型的列表
    # cluster_info 为 clusterInfo 类的实例

    # 检查功耗超限次数是否达到阈值, 如果是则标记该主机, 并且将其中部分pod迁出
    nodelist = []
    powerRecord = cluser_info.powerRecord
    for key, value in powerRecord.item():
        if value > 8:
            nodelist.append(key)
        
    # 此时nodelist是需要迁出的主机列表, 同时也是需要禁用的主机列表
    for node in nodelist:
        migrateQueue += selectPodfromHost(pod_list[node], node)
    
    # 除此之外还需要导出需要休眠的主机列表

    # 此时已经获得pod列表, 需要判断迁移列表是否为空 ?
    return len(migrateQueue)

def checkCost():
    # 检查能耗价格? 这个似乎无需在意吧 ?
    # 暂时不实现这个函数
    return

def beginMigrate():
    # 实现迁移逻辑
    # 首先标记禁止迁入迁出的主机
    # 接着触发被动迁移
    # 最后解除主机标记
    # 问题在于如何获取迁移状态, 即迁移是否完成 ?
    # 还需要统计每个pod的状态!!!

    # 调用迁移接口
    if len(migrateQueue) == 0:
        return
    
    # 还需要考虑是否要真正的迁移，要处理防误触
    
    migrateQueue = mAPI.migratePod(migrateQueue)
    return

def getPodFromHost(host_name, ip):
    # 通过mysql来获得host_name上的所有pod信息，这些信息都是podInfo类型的
    pod_list = []
    # 从数据库中获取也是可以的
    db_tool = MySQLTool(host='192.168.1.201', username='ecm', password='123456', database='ecm')
    # 还是需要做限制的，要去除过期数据

    # 这里还有一个视图，为 latest_poddata，针对每个pod仅显示一次
    
    result = db_tool.select('latest_poddata', columns=['*'])
    for dict in result:
        print(dict)
        pod = podInfo()
        pod.pod_name = dict['pod_name']
        pod.host_name = host_name
        pod.cpu_load = dict['cpu_load']
        pod.mem_load = dict['memory_load']
        pod_list.append(pod)
    # 需要更新power与status
    db_tool.close()
    return pod_list

def getPodList(host_list):
    # 构造字典, key为节点名称, value为podInfo类型的列表
    # 从哪儿获得数据呢？从api
    pod_list = []
    
    for key, value in host_list.item():
        pod_list += getPodFromHost(key, value)
    return pod_list

def run():
    # 用于实现迁移触发流程，循环检查是否满足触发条件
    cluster = clusterInfo()
    pod_list = getPodList(cluster.hostList)

    while True:
        cluster.update()
        que = checkPowerLimit(pod_list, cluster)
        if len(que) > 0:
            migrateQueue += que
        beginMigrate()
        time.sleep(10)

def test():
    for pod in getPodFromHost("node1", "1"):
        pod.getInfo()
        # print(pod)

test()