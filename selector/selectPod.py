# 最终输出的是一个列表，即migrateQueue
# 同时要负责锁定某些主机，并保存锁定列表，在迁移完成之后解除锁定
# 周期性扫描？
# 维护信息列表
# 周期性测试是否满足触发条件
import os
import sys
import time

home_dir = os.path.expanduser("~")
sys.path.append(home_dir, '/container_migrate/migrate', 'migrate.py')
import migrate.apiserver as mAPI

import clusterInfo
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
    
    
    migrateQueue = mAPI.migratePod(migrateQueue)

    return


def getPodList():
    # 构造字典, key为节点名称, value为podInfo类型的列表
    pass

def run():
    cluster = clusterInfo()
    pod_list = getPodList()

    while True:
        cluster.update()
        que = checkPowerLimit(pod_list, cluster)
        if len(que) > 0:
            migrateQueue += que
        beginMigrate()
        time.sleep(10)










cluster = clusterInfo()
cluster.getInfo()
cluster.update()
if(checkCost(cluster)):
    # 标记主机 ?
    beginMigrate()
if(checkPowerLimit(cluster)):
    # 标记主机 ?
    beginMigrate()
