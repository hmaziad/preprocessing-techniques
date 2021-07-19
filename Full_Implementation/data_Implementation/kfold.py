import numpy as np
from sklearn.model_selection import KFold
import json

# array of length 10
# arr = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
# print("Array Length: ", len(arr))


def pretty(d, indent=0):
    for key, value in d.items():
        print("\t" * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print("\t" * (indent + 1) + str(value))


def getIndices_trn_tst(arr, k):
    kf = KFold(n_splits=k)
    trainIndices = {}
    count = 0
    for train_index, test_index in kf.split(arr):
        # print("TRAIN:", train_index, "TEST:", test_index)
        trainIndices[str(count)] = {"train": train_index, "test": test_index}
        count = count + 1
    return trainIndices
    # pretty(trainIndices)
    # print(json.dumps(trainIndices))


# for i in range(2, 6):
#     print("K = ", i)
#     getIndices_trn_tst(arr, i)
#     print()
#     print("*******************")
#     print()
