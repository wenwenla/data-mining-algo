import numpy as np
from collections import defaultdict

def createDataSet(filePath):
    data, label = [], []
    with open(filePath, 'r') as fin:
        label_mp = {
            'largeDoses': 0,
            'smallDoses': 1,
            'didntLike': 2,
        }
        for line in fin:
            tmp = line.split()
            data.append(list(map(float, tmp[0:3])))
            label.append(label_mp[tmp[3]])
    return (np.array(data), np.array(label))


def autoNorm(data):
    mn = np.min(data, axis=0)
    mx = np.max(data, axis=0)
    return (data - mn) / (mx - mn)


def classify(trainData, trainLabel, testData, k):
    dist = np.sum((testData - trainData) ** 2, axis=1)
    sortedData = sorted(zip(dist, trainLabel))
    k = min(k, len(sortedData))
    keyCnt = defaultdict(int)
    for i in range(k):
        key = sortedData[i][1]
        keyCnt[key] += 1
    return max(zip(keyCnt.values(), keyCnt.keys()))[1]


if __name__ == '__main__':
    data, lable = createDataSet('./datingTestSet.txt')
    data = autoNorm(data)

    trainData, trainLabel = data[0:700], lable[0:700]
    testData, testLabel = data[700:], lable[700:]

    goodCnt, totalCnt = 0, 0
    for td, tv in zip(testData, testLabel):
        predictVal = classify(trainData, trainLabel, td, 20)
        if predictVal == tv:
            goodCnt += 1
        totalCnt += 1
    print('Acc: {}'.format(goodCnt / totalCnt))