import os
from driver import trainModel
from driver import testData

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# datapath = (
#     # ROOT_DIR
#     # + "/Hussein/data/pairs"
#     # + "/Full_Implementation/data_Implementation/data/pairs"
#     ROOT_DIR
#     + "/Full_Implementation/data_Implementation/data/history/k_5/iteration_"
# )

targetPath = ROOT_DIR+ "/Full_Implementation/data_Implementation/data/history"
for intersect in [1,0]:
    targetPath1 = targetPath
    if(intersect):
        targetPath1 = targetPath1 + "/intersect"
    else:
        targetPath1 = targetPath1 + "/union"
    for historyPercentage in [0,10,30,50,100]: # history percentage
        targetPath2 = targetPath1+"/"+str(historyPercentage)+"_history"
        for k in [3,5,10]:
            targetPath3 = targetPath2 + "/k_"+str(k)
            for iteration in range(0,k):
                targetPath4 = targetPath3 + "/iteration_"+str(iteration)
                print('***** targetPath: ',targetPath4 , "**********")
                trainModel(targetPath4, targetPath4 + "/NN_Model.p")

# trainingFileName = "/alldialogues_trn.p"
# testingFileName = "/alldialogues_tst.p"
# for i in range(0,5):
#     newPath = (datapath+str(i))
#     print("*****Path: ",newPath)
#     testData(newPath, newPath + "/NN_Model.p")
# for i in range(0,5):
#     newPath = (datapath+str(i))
#     trainModel(newPath, newPath + "/NN_Model.p")


