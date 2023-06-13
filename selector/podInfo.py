# 负责统计pod相关的信息, 重点是是pod的功耗、所在主机、资源利用率、其他标签信息等等等
import os
import sys
home_dir = os.path.expanduser("~")
sys.path.append(home_dir+'/container_migrate/migrate')
import apiserver as mAPI

class podInfo:
    def __init__(self):
        self.pod_name = ""
        self.host_name = ""
        self.power = 0
        self.cpu_load = 0
        self.mem_load = 0
        self.status = 0
    
    def __lt__(self, other):
        # 按照功耗降序
        return self.power > other.power

    def getInfo(self):
        ret = {}
        ret['pod_name'] = self.pod_name
        ret['host_name'] = self.host_name
        ret['power'] = self.power
        ret['cpu_load'] = self.cpu_load
        ret['mem_load'] = self.mem_load
        ret['status'] = self.status

        return ret

    def updata(self):
        # 主要是更新status
        # 通过轮训的方式 ?
        # 更新host_name以及power、cpu_load mem_load还有status？
        # self.host_name, self.status = mAPI.getPodInfo(self.pod_name)
        self.host_name = mAPI.getPodHost(self.pod_name)
        self.status = mAPI.getPodStatus(self.pod_name)
        # print(mAPI.getPodInfo(self.pod_name))
        return
    

# 新建一个列表, 接着通过循环新建并加入

