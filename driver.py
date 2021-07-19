import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
pairs_path = ROOT_DIR + "/original_data_cleaning/data/cleaned_data"
history_path = ROOT_DIR + "/history_implementation/data"
context_path = ROOT_DIR + "/Hussein/data/context"
test_path = ROOT_DIR + "/Hussein/data/pairs"
test_datapath = (
    ROOT_DIR
    # + "/Full_Implementation/data_Implementation/data/test/history_implementation"
    + "/Full_Implementation/data_Implementation/data/history/k_3/iteration_0"
)


pairs_model = ROOT_DIR + "/pairs_implementation/pairs_model.p"
history_model = ROOT_DIR + "/history_implementation/history_model.p"
context_model = ROOT_DIR + "/Hussein/context_model.p"
test_model = ROOT_DIR + "/Full_Implementation/data_Implementation/data/history/k_3/iteration_0/NN_Model.p"

## Data Cleaning
def generateCleanData():
    from original_data_cleaning.dialoguesreorganization import cleanDriver

    cleanDriver()


## Implementations
def trainModel(data_path, model_path):
    from seq2seq import trainingDriver

    trainingDriver(data_path, model_path)


def testData(data_path, model_path):
    from seq2seq import testDriver

    testDriver(data_path, model_path)


def evaluateModel(str, data_path, model_path):
    from seq2seq import evaluateDriver

    evaluateDriver(str, data_path, model_path)


# trainModel(test_datapath, test_model)
# testData(test_datapath, test_model)
# trainModel(pairs_path, pairs_model)
# testData(pairs_path, pairs_model)
# trainModel(context_path, context_path)
# testData(context_path, context_path)
