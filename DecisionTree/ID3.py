from math import log
from collections import defaultdict


class TNode(object):

    def __init__(self):
        self.child = []
        self.edge = None
        self.parent = None
        self.axis = None
        self.label = None
    
    def addChild(self, node, attr, axis):
        if node is None:
            return
        self.child.append(node)
        if not self.axis:
            self.axis = axis
        node.edge = attr
        node.parent = self

    def setLabel(self, label):
        self.label = label

    def __str__(self):
        return 'axis: {} edge: {} label: {}'.format(self.axis, self.edge, self.label)


def createDataSet(fileName):
    with open(fileName, 'rb') as fin:
        data, val = [], []
        for line in fin:
            line = line.decode('utf8').split()
            data.append(tuple(line[:-1]))
            val.append(line[-1])
    return list(zip(data, val))


def shannonEnt(data):
    total = len(data)
    classCnt = defaultdict(int)
    for d in data:
        classCnt[d[1]] += 1
    s = 0.0
    for k, v in classCnt.items():
        s -= (v / total) * log(v / total, 2)
    return s


def gain(data, axis):
    attrs = defaultdict(list)
    for d in data:
        attrs[d[0][axis]].append(d)
    s = 0.0
    total = len(data)
    for k, v in attrs.items():
        # print(k)
        # print(shannonEnt(v))
        s += shannonEnt(v) * len(v) / total
    return shannonEnt(data) - s


def tree(data, axisSet):
    # print(data)
    # print(axisSet)
    # print('=' * 20)
    root = TNode()
    if len(axisSet) == 0:
        lbmx = defaultdict(int)
        for d in data:
            lbmx[d[1]] += 1
        nowLabel = max(zip(lbmx.values(), lbmx.keys()))[1]
        root.setLabel(nowLabel)
        return root
    lbset = set()
    for d in data:
        lbset.add(d[1])
    if len(lbset) == 1:
        root.setLabel(data[0][1])
        return root

    mx = -1
    best = -1
    for i in axisSet:
        nowGain = gain(data, i)
        if nowGain > mx:
            mx = nowGain
            best = i
    assert best != -1
    splited = defaultdict(list)
    for d in data:
        splited[d[0][best]].append(d)

    for k, v in splited.items():
        root.addChild(tree(v, axisSet - {best}), k, best)

    return root

def printTree(tnode):
    print(tnode)
    for nxt in tnode.child:
        printTree(nxt)


if __name__ == '__main__':
    data = createDataSet('./watermelon2_0.txt')
    print(data)
    print(gain(data, 0))
    tr = tree(data, set(range(len(data[0][0]))))
    printTree(tr)