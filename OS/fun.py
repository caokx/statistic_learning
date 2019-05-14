import numpy as np

RL = [[], [], []]  # 就绪队列2， 1， 0，存放PID
BL = []  # 阻塞队列

RUN = []  # 记录当前运行程序的PID

PL = []   # 记录进程name，索引代表进程PID
PCBL = []  # 记录进程PCB，索引代表进程PID
RCBL = []

class PCB(object):
    def __init__(self, PID, priority):
        # 初始进程
        self.PID = PID
        self.statue = 1  # 0='block';1='ready';2='running'
        self.priority = priority  # 0='init',1='user',2='system'
        self.source = [0, 0, 0, 0]
        self.request = [0, 0, 0, 0]
        self.parent = []
        self.child = []

class RCB(object):
    def __init__(self, RID, K):
        self.RID = RID  #
        self.K = K  # 资源总数
        self.U = K  # 可利用资源数
        self.WL = []  # 等待列表

def scheduler():
    # 找到最高优先级进程
    for i in range(2, -1, -1):
        for j in range(len(RL[i])):
            PCBL[RUN[0]].statue = 1
            RUN[0] = RL[i][0]
            PCBL[RUN[0]].statue = 2
            return

def init():
    RL[0].append(0)
    PCBL.append(PCB('init', 0))
    PL.append('init')
    PCBL[-1].parent = [0]
    RUN.append(0)
    PCBL[RUN[0]].statue = 2  # 标记为runing
    return 0

def create(Pname, priority):
    # 创建进程
    PCBL.append(PCB(len(PL), priority))
    PL.append(Pname)
    PCBL[-1].parent.append(RUN[0])
    PCBL[RUN[0]].child.append(len(PL)-1)
    insertRL(priority, len(PL)-1)   # 传入优先级和PID
    return 0

def delete(Pname):
    index = PL.index(Pname)
    for i in range(len(PCBL[index].child)):
        delete(PL[PCBL[index].child[i]])
        # PCBL[index].child.pop(PL[PCBL[index]])

    for i in range(4):
        RCBL[i].U += PCBL[index].source[i]
        PCBL[index].source[i] = 0

    if PCBL[index].statue == 1:
        RL[PCBL[index].statue].remove(index)
        return
    elif PCBL[index].statue == 0:
        PCBL[index].statue = -1
        BL.remove(index)
        for i in range(4):
            if index in RCBL[i].WL:
                RCBL[i].WL.remove(index)
        return
    elif PCBL[index].statue == 2:
        PCBL[index].statue = -1
        RL[PCBL[index].priority].remove(index)
        for i in range(2, -1, -1):
            for j in range(len(RL[i])):
                PCBL[RUN[0]].statue = 0
                RUN[0] = RL[i][0]
                PCBL[RUN[0]].statue = 2
                return
    return

def request(R, num):  # 资源类型，资源数量
    if R.U >= num:
        PCBL[RUN[0]].source[R.RID-1] += num
        R.U -= num
        return
    else:
        R.WL.append(RUN[0])
        BL.append(RUN[0])
        PCBL[RUN[0]].statue = 0
        PCBL[RUN[0]].request[R.RID-1] = num
        RL[PCBL[RUN[0]].priority].remove(RUN[0])
        for i in range(2, -1, -1):
            for j in range(len(RL[i])):
                RUN[0] = RL[i][0]
                PCBL[RUN[0]].statue = 2
                return

def awake():
    for i in range(4):
        for j in range(len(RCBL[i].WL)):
            if PCBL[RCBL[i].WL[j]].request[i] <= RCBL[i].U:
                RCBL[i].U -= PCBL[RCBL[i].WL[j]].request[i]
                PCBL[RCBL[i].WL[j]].source[i] += PCBL[RCBL[i].WL[0]].request[i]
                PCBL[RCBL[i].WL[j]].request[i] = 0
                temp = RCBL[i].WL[j]
                RCBL[i].WL.remove(temp)
                if PCBL[temp].request == [0, 0, 0, 0]:
                    BL.remove(temp)
                    PCBL[temp].statue = 1
                    RL[PCBL[temp].priority].append(temp)
    return

def TO():
    # 模拟时钟中断
    PCBL[RUN[0]].statue = 1
    for i in range(2, -1, -1):
        for j in range(len(RL[i])):
            temp = RL[i].pop(0)
            RL[i].append(temp)
            RUN[0] = RL[i][0]
            PCBL[RUN[0]].statue = 2
            return 0

def insertRL(priority, PID):
    RL[priority].append(PID)
    return







