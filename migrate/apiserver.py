#支持中文
#导入包
#-- coding: UTF-8 --
#!/usr/bin/env python3
from kubernetes import client, config
import xmlrpc.client
import subprocess


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

def migratePod(pod_name):
    # 迁出pod_name的pod
    # 通过删除该pod,并重启的方式进行迁出
    # 命名空间为默认空间
    # 返回迁移后的主机名
    print(pod_name)

    # 挨个迁移每一个pod，阻塞的哦
    command = ["kubectl", "delete", "pod", pod_name]
    subprocess.run(command, check=True) # 该命令是阻塞的,非常棒
    #验证pod的状态,当其为Running时才返回
    status = getPodStatus(pod_name)
    while status != "Running":
        status = getPodStatus(pod_name)
        if status == "Failed":
            return "Failed"
    
    return getPodHost(pod_name)

def banHost(host_name):
    # 直接执行命令即可, 禁止pod调入
    command = ["kubectl", "cordon", host_name]
    subprocess.run(command, check=True)
    

def unbanHost(host_name):
    # 直接执行命令即可, 取消节点限制
    command = ["kubectl", "uncordon", host_name]
    subprocess.run(command, check=True)

def getPodStatus(pod_name):
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

def getPodHost(pod_name):
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
    return pod.spec.node_name


def predictPower(cpu_load, mem_load):
    # 导入预测模块，减去静态功耗
    # 创建服务器代理
    # print("oooo:", cpu_load, mem_load)
    try:
        server = xmlrpc.client.ServerProxy("http://192.168.1.201:9926")
        # 输入参数
        # 调用方法
        v1 = server.predictPower(cpu_load, mem_load)
        v2 = server.predictPower(0, 0)
        result = float(v1) - float(v2)
        # print(result)
    except Exception as e:
        print(e)
        return
    return result

# print(getStatus("test-scheduler-5659b79dc9-5bxdg"))