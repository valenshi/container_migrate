# 负责统计pod相关的信息, 重点是是pod的功耗、所在主机、资源利用率、其他标签信息等等等
class podInfo:
    def __init__(self):
        self.podname = ""
        self.hostname = ""
        self.power = 0
        self.cpuLoad = 0
        self.memLoad = 0
        self.status = 0

    def getInfo(self):
        pass

    def updata(self):
        # 主要是更新status
        # 通过轮训的方式 ?
        pass
    

# 新建一个列表, 接着通过循环新建并加入
podlist = []
podlist.append(podInfo())
