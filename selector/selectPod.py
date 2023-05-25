# 最终输出的是一个列表，即migrateQueue
# 同时要负责锁定某些主机，并保存锁定列表，在迁移完成之后解除锁定
# 周期性扫描？
# 维护信息列表
# 周期性测试是否满足触发条件
import clusterInfo



def checkPowerLimit(self):
    # 检查功耗超限次数是否达到阈值, 如果是则标记该主机, 并且将其中部分pod迁出
    return

def checkCost(self):
    # 检查能耗价格? 这个似乎无需在意吧 ?
    # 暂时不实现这个函数
    return

def beginMigrate(self):
    # 实现迁移逻辑
    # 首先标记禁止迁入迁出的主机
    # 接着触发被动迁移
    # 最后解除主机标记
    # 问题在于如何获取迁移状态, 即迁移是否完成 ?
    # 还需要统计每个pod的状态!!!
    return


cluster = clusterInfo()
cluster.getInfo()
cluster.update()
if(checkCost(cluster)):
    # 标记主机 ?
    beginMigrate()
if(checkPowerLimit(cluster)):
    # 标记主机 ?
    beginMigrate()
