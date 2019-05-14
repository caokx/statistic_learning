import numpy as np
from fun import *


def input():
    result = []
    result.append(PL[RUN[0]])
    with open('input', 'r') as f:
        for line in f.readlines():
            command = line.split()
            if command[0] == 'cr':
                create(command[1], int(command[2]))
                scheduler()
                result.append('\n')
                result.append(PL[RUN[0]])
            elif command[0] == 'to':
                TO()
                result.append('\n')
                result.append(PL[RUN[0]])
            elif command[0] == 'req':
                request(eval(command[1]), int(command[2]))
                result.append('\n')
                result.append(PL[RUN[0]])
            elif command[0] == 'de':
                delete(command[1])
                awake()
                scheduler()
                result.append('\n')
                result.append(PL[RUN[0]])
            else:
                continue
    return result


def output(result):
    with open('output', 'w') as t:
        t.writelines(result)
    t.close()


if __name__ == '__main__':
    init()  # 初始化

    R1 = RCB(1, 1)
    R2 = RCB(2, 2)
    R3 = RCB(3, 3)
    R4 = RCB(4, 4)
    RCBL.append(R1)
    RCBL.append(R2)
    RCBL.append(R3)
    RCBL.append(R4)

    result = input()
    output(result)



