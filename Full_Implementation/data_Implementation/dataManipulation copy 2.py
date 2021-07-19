import pickle
import os
import random
import math
import copy
from KB_functions import getCommonTermsIntersection
from KB_functions import getCommonTermsUnion
from kfold import getIndices_trn_tst
from pathlib import Path
from collections import Counter

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
pairsPath = ROOT_DIR + "/data/pairs/alldialogues.p"
historyPath = ROOT_DIR + "/data/history/alldialogues.p"
filterWords = [
    "italian",
    "food",
    "morning",
    "<SILENCE>",
    "paris",
    "si x",
    "people",
    "cheap",
    "do",
    "price",
    "two",
    "madrid",
    "spanish",
    "no",
    "not",
    "work",
    "something",
    "else",
    "perfect",
    "phone",
    "number",
    "restaurant",
    "thanks",
    "thank",
    "hello",
    "love",
    "indian",
    "bombay",
    "four",
    "french",
    "cuisine",
    "don't",
    "hi",
    "address",
    "british",
    "great",
    "rock",
    "london",
    "rome",
    "moderate",
    "eight",
    "reservation",
    "expensive",
]


def parseDialogueFromFile(path):
    objects = []
    with (open(path, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    sampleIndex = random.randrange(800)
    # print("sampleIndex",sampleIndex)
    return [objects[0][sampleIndex]]
    # return objects[0]


def getDialogueWithHistory(dialogues):
    dialoguesWithHistory = copy.deepcopy(dialogues)

    for dialogue in dialoguesWithHistory:
        userRequest = ""
        for pair in dialogue:
            pair[0] = pair[0] + " " + userRequest
            userRequest = pair[0]
    return dialoguesWithHistory


def writeToFile(path, dialogues):
    pickle_out = open(path, "wb")
    pickle.dump(dialogues, pickle_out)
    pickle_out.close()


def getFilteredDialogue(dialogues):
    dialogues = copy.deepcopy(dialogues)
    for dialogue in dialogues:
        for pair in dialogue:
            userRequest = pair[0]
            editedRequest = ""
            for word in userRequest.split(" "):
                if word in filterWords:
                    editedRequest = (editedRequest + " " + word).strip()
            pair[0] = editedRequest
    return dialogues


def getKBIntegrateDialogueUserRequest(dialogues,intersect):
    dialogues = copy.deepcopy(dialogues)
    for dialogue in dialogues:
        for pair in dialogue:
            userRequest = pair[0]
            if(intersect):
                commonTerms = " ".join(getCommonTermsIntersection(userRequest))
            else:
                commonTerms = " ".join(getCommonTermsUnion(userRequest))
            if len(commonTerms) > 0:
                pair[0] = userRequest + " " + commonTerms
    return dialogues


def getKBIntegrateDialogueBotRequest(dialogues):
    dialogues = copy.deepcopy(dialogues)
    for dialogue in dialogues:
        for pair in dialogue:
            botRequest = pair[1]
            commonTerms = " ".join(getCommonTermsIntersection(botRequest))
            pair[1] = (botRequest + " " + commonTerms).strip()
    return dialogues


def printRandomSample(dialogues):
    # sampleIndex = random.randrange(800)
    # sampleIndex = 615
    sampleIndex = 0
    # print("sampleIndex: ", sampleIndex)
    sampleDialogue = dialogues[sampleIndex]
    for i in range(len(sampleDialogue)):
        print(i, ": ", sampleDialogue[i])
        print()


def writeToFile(path, dialogues):
    pickle_out = open(path, "wb")
    pickle.dump(dialogues, pickle_out)
    pickle_out.close()


def createDataFromKFold(k,targetPath, dialoguesPath):
    # dialogues = parseDialogueFromFile(dialoguesPath)
    dialogues = dialoguesPath
    indicesDictionary = getIndices_trn_tst(dialogues, k)
    for key, value in indicesDictionary.items():
        mypath = targetPath + "/k_" + str(k) + "/iteration_" + key

        trainingSet = [dialogues[index] for index in value["train"]]
        testingSet = [dialogues[index] for index in value["test"]]
        # print(len(trainingSet))
        # print(len(testingSet))
        trainingFilename = "/alldialogues_trn.p"
        testingFilename = "/alldialogues_tst.p"
        Path(mypath).mkdir(parents=True, exist_ok=True)

        writeToFile(mypath + trainingFilename, trainingSet)
        writeToFile(mypath + testingFilename, testingSet)

        print("**************")
        # print('train: ',index.train)
        # print('test: ',index.test)


def getHistoryPercentage(dialogues, percentage):
    dialogues = copy.deepcopy(dialogues)
    if(percentage == 0):
        return dialogues
    for dialogue in dialogues:
        prevUserRequest = []
        for pair in dialogue:
            pair[0] = (pair[0] + " " + " ".join(prevUserRequest)).strip()
            pairAsArr = pair[0].split(" ")
            prevUserRequest = pairAsArr[: int(len(pairAsArr) // (float(100 / percentage)))]
    return dialogues

def getHistoryPercentageWithKeepOnlyDuplicates(dialogues, percentage):
    dialogues = copy.deepcopy(dialogues)
    count = 0
    # if(percentage == 0):
    #     return dialogues
    for dialogue in dialogues:
        prevUserRequest = []
        predicates =  {
                "beijing": "R_location",
                "seoul": "R_location",
                "rome": "R_location",
                "london": "R_location",
                "tokyo": "R_location",
                "bombay": "R_location",
                "madrid": "R_location",
                "paris": "R_location",
                "hanoi": "R_location",
                "bangkok": "R_location",

                "two": "R_number",
                "four": "R_number",
                "six": "R_number",
                "eight": "R_number",

                "vietnamese": "R_cuisine",
                "spanish": "R_cuisine",
                "korean": "R_cuisine",
                "thai": "R_cuisine",
                "japanese": "R_cuisine",
                "cantonese": "R_cuisine",
                "british": "R_cuisine",
                "italian": "R_cuisine",
                "indian": "R_cuisine",
                "french": "R_cuisine",

                "expensive": "R_price",
                "cheap": "R_price",
                "moderate": "R_price",

                # "phone": "R_phone",
                # "address": "R_address",

                # numbers are ratings
            }
        toRequest = { 
            "R_location": "",
            "R_number": "",
            "R_rating": "",
            # "R_address": "",
            "R_price": "",
            "R_cuisine": "",
            # "R_phone": "",
             }
        for pair in dialogue:
            nonRestoWords = [word for word in pair[0].split(" ") if not word.startswith('resto')]

            predFound = False
            for key in predicates.keys():
                for word in nonRestoWords:
                    if word == key:
                        predFound = True
                        toRequest[predicates.get(key)] = key
             
            # restoWordsPair = [word for word in pair[0].split(" ") if word.startswith('resto')]
            # restoWordsPrevPair = [word for word in prevUserRequest if word.startswith('resto')]
            wordsFromKB = []
            # print("********nonRestoWords: ",nonRestoWords)
            # print("********toRequest: ",toRequest)
            # print("********restoWordsPair: ",restoWordsPair)
            # print("********restoWordsPrevPair: ",restoWordsPrevPair)
            # print("\n\n\n")
            # if(len(restoWordsPrevPair) != 0 and len(restoWordsPair) != 0 ):
            #     intersectionOfWords = list(set(restoWordsPair) & set(restoWordsPrevPair)) 
            
            # elif(len(restoWordsPrevPair) == 0 and len(restoWordsPair) != 0):
            #     intersectionOfWords = restoWordsPair
            # elif(len(restoWordsPrevPair) != 0 and len(restoWordsPair) == 0):
            #     intersectionOfWords = restoWordsPrevPair
            # if(len(intersectionOfWords) == 0):
           
            # print(nonRestoWords,"////////",prevUserRequest)

            # else:
            request = ""
            for key in toRequest.keys():
                request = request + " " + toRequest.get(key)
            wordsFromKB = getCommonTermsIntersection(request.strip())

            # if(len(wordsFromKB) == 0):
            #     intersectionOfWords = restoWordsPrevPair

            if(not predFound):
                # print("intersectionOfWords",prevUserRequest[:int(math.ceil(len(prevUserRequest)/(100/percentage)))])
                if( percentage == 0):
                    wordsFromKB = prevUserRequest[:0]
                else:    
                    wordsFromKB = prevUserRequest[:int(math.ceil(len(prevUserRequest)/(100/percentage)))]

            # if(not predFound):
            #     count = count +1
            #     print("count",count)
            #     # print("took half",math.ceil(len(intersectionOfWords)/(100/percentage)) ," ", len(intersectionOfWords))
            #     print("before",len(intersectionOfWords))
            #     intersectionOfWords = intersectionOfWords[:math.ceil(len(intersectionOfWords)/(100/percentage))]
            #     print("after",len(intersectionOfWords))
            # print("nonRestoWords: ",nonRestoWords)
            # allWords = (pair[0] + " " + " ".join(prevUserRequest)).strip().split(" ")
            # counts = Counter(allWords)
            # dupWords = [word for word in allWords if counts[word] > 1]
            # print("dupWords: ", dupWords)

            # print("Predicate: ",predFound)
            # print("intersectionOfWords: ",intersectionOfWords)
            # print(math.ceil(len(intersectionOfWords)/(100/percentage)))
            # intersectionOfWords = intersectionOfWords[] predFound
            # intersectionOfWords[:math.ceil(len(intersectionOfWords)/(100/percentage))]
            # intersectionOfWordsToPrint = intersectionOfWords[:math.ceil(len(intersectionOfWords)/(100/percentage))]
            # intersectionOfWords = intersectionOfWordsToPrint if not predFound else intersectionOfWords

       

            pair[0] = (" ".join(nonRestoWords).strip() + " " + " ".join(wordsFromKB).strip()).strip()
            # print("RESULT pair to print",pair[0])
            prevUserRequest =  wordsFromKB

            # print("Result: ", pair[0] )
            # prevUserRequest = pairAsArr
    return dialogues

    

# createDataFromKFold(5,(getFilteredDialogue(parseDialogueFromFile(historyPath))))
srcDialoguesPath = ROOT_DIR + "/data/test/pairs/alldialogues.p"
# targetPath = ROOT_DIR + "/data/history/intersect/0_history"
# targetPath = ROOT_DIR + "/data/history"

targetPath = ROOT_DIR + "/data/history_converge"
# print("srcDialoguesPath: ",srcDialoguesPath)
# # printRandomSample((parseDialogueFromFile(srcDialoguesPath)))
targetPath1 = targetPath
# for historyPercentage in [0]: # history percentage
#     targetPath2 = targetPath1+"/"+str(historyPercentage)+"_history"
#     for k in [5]:
#         print('targetPath: ',targetPath2)
#         createDataFromKFold(k,targetPath2,getHistoryPercentageWithKeepOnlyDuplicates((parseDialogueFromFile( srcDialoguesPath )  ), historyPercentage))
        
newCustomPath  =   ROOT_DIR + "/data/history_converge/0_history/k_5/iteration_0/alldialogues_trn.p"
# printRandomSample(getHistoryPercentageWithKeepOnlyDuplicates(parseDialogueFromFile(srcDialoguesPath),0))
# printRandomSample(getHistoryPercentageWithKeepOnlyDuplicates(parseDialogueFromFile(srcDialoguesPath),0))
# newCustomPath  =   ROOT_DIR + "/data/history_converge/10_history/k_5/iteration_0/alldialogues_trn.p"
printRandomSample(parseDialogueFromFile(newCustomPath))
# newCustomPath  =   ROOT_DIR + "/data/history_converge/25_history/k_5/iteration_0/alldialogues_trn.p"
# printRandomSample(parseDialogueFromFile(newCustomPath))


# createDataFromKFold(10,targetPath,getHistoryPercentage(getKBIntegrateDialogueUserRequest(parseDialogueFromFile(srcDialoguesPath),1), 0))
# printRandomSample(parseDialogueFromFile(
#     # getHistoryPercentage((parseDialogueFromFile(srcDialoguesPath)), 51)
#     ROOT_DIR + "/data/history_kb/0_history/k_10/iteration_0/alldialogues_trn.p"
# ))
# printRandomSample(getHistoryPercentageWithKeepOnlyDuplicates(getKBIntegrateDialogueUserRequest(parseDialogueFromFile(newCustomPath),1), 100))

# thisPath =  ROOT_DIR + "/data/history_kb_KD/100_history/k_5/iteration_0/alldialogues_trn.p"
# print("////////",thisPath,"//////////")
# printRandomSample(parseDialogueFromFile(thisPath))

# printRandomSample(parseDialogueFromFile(
#     ROOT_DIR + "/data/history_converge/100_history/k_5/iteration_0/alldialogues_trn.p"
# ))

# print(indicesDictionary)


# Path(mypath).mkdir(parents=True, exist_ok=True)
# print("good here")
# writeToFile(mypath+fileName,(parseDialogueFromFile(historyPath)))
# mypath = ROOT_DIR + "/data/history/k_3/iteration_0"
# fileName = "/alldialogues_trn.p"
# printRandomSample(parseDialogueFromFile(mypath + fileName))


# path = ROOT_DIR + "/data/test/history_implementation/alldialogues.p"
# # printRandomSample()
# print(len(parseDialogueFromFile(path)))
# createDataFromKFold(10, historyPath)
# makeDirectorys(3, historyPath)
