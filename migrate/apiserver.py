#支持中文
#导入包

# 直接调用虚拟机迁移脚本或命令
def migrateVM(vm_name, target_node):
    #首先导入环境变量
    #其次执行迁移命令(这里假设迁移指令必然合法)
    #返回执行的结果
    msg = "ok 200"
    return msg

def excludeHost(host_list):
    # 排除主机，通过执行kubectl相关命令将所有pod迁出
    # 将主机设为休眠状态

    # 返回、修改主机的状态
    pass

def migratePod(migrateQueue):
    # 迁出pod列表，通过重启pod形式
    print(migrateQueue)
    # 这里应该分为两类，一种是迁出部分pod，一种是迁出全部pod，两种应该区别对待！

    # 如果杀死了pod，那么重新启动的pod又如何保证名称相同呢？
    # 可以通过部署的时候yaml文件来指定默认名称

    # 直接执行删除命令来删除某个pod

    # 挨个迁移每一个pod，监控迁移周期，当迁移成功之后才会迁移下一个

    migrateQueue = []
    return migrateQueue

def banHost(host_list):
    # 直接执行命令即可
    pass

def unbanHost(host_list):
    # 直接执行命令即可
    pass


def getStatus(pod):
    # 通过pod name来获取其状态
    # 分为running?pending?error?crash等等
    pass

def predictPower(cpu_load, mem_load):
    # 通过调用预测脚本, 来统一预测实时功耗
    # 直接将预测脚本内置进来, 这样会速度快一些
    pass