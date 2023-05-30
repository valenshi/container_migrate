#支持中文
#导入包
from kubernetes import client, config

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


def getStatus(pod_name):
    # Kubernetes中Pod的状态可以分为以下几种：
    # Pending：Pod已被创建，但是尚未被调度到节点上运行。
    # Running：Pod已经被调度到节点上并且正在运行中。
    # Succeeded：Pod已经成功完成了所有工作。
    # Failed：Pod已经完成了所有工作，但返回一个非零的退出码。
    # Unknown：无法获取Pod的状态信息，通常是由于调度器或其他组件出现故障所致。
    # 加载Kubeconfig文件

    config.load_kube_config()

    # 创建核心V1 API客户端
    v1 = client.CoreV1Api()

    # 检查Pod是否存在
    try:
        pod = v1.read_namespaced_pod(name=pod_name, namespace='default')
    except client.rest.ApiException as e:
        if e.status == 404:
            return "Overdue"
        else:
            raise e

    # 如果Pod存在，则返回其状态
    return pod.status.phase

def predictPower(cpu_load, mem_load):
    pass

# print(getStatus("test-scheduler-5659b79dc9-5bxdg"))