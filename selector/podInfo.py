# 负责统计pod相关的信息, 重点是是pod的功耗、所在主机、资源利用率、其他标签信息等等等
class podInfo:
    def __init__(self):
        self.pod_name = ""
        self.host_name = ""
        self.power = 0
        self.cpu_load = 0
        self.mem_load = 0
        self.status = 0

    def getInfo(self):
        print("pod_name: ", self.pod_name)
        print("host_name: ", self.host_name)
        print("power: ", self.power)
        print("cpu_load: ", self.cpu_load)
        print("mem_load: ", self.mem_load)
        print("status: ", self.status)

    def updata(self):
        # 主要是更新status
        # 通过轮训的方式 ?
        pass
    

# 新建一个列表, 接着通过循环新建并加入

