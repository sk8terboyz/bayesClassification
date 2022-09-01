from tkinter import *
from tkinter import ttk
import nltk
from array import *
import re

titles = []
features = []
testing = []
data = []
correct = 0
failed = 0
overallConsistency = []
classifications = []


# Load file and start reading the meta files
def loadMeta():
    try:
        filename = (metaTxt.get())
        # Update user on progress
        outputLabel = ttk.Label(frm, text="Reading "+metaTxt.get()+"...", padding=5).grid(column=2,row=10)
        with open(filename) as f:
            print(filename)
            lines = f.readlines()
            titleCount = 0
            classificationFlag = False
            for line in lines:
                sepFeatures = []
                featureCount = 0
                for word in line.split(','):
                    if ":" in word:
                        count = 0
                        for key in word.split(':'):
                            # do same work here as when a colon isn't present
                            if(key == "class"):
                                classificationFlag = True
                            if(not classificationFlag):
                                if(count == 0):
                                    # Read each title
                                    titles.append(key)
                                    count += 1
                                    titleCount += 1
                                else:
                                    # Read in feature after the title
                                    sepFeatures.append(key)
                            else:
                                if(key == "class"):
                                    titles.append(key)
                                else:
                                    classifications.append(key)
                    else:
                        key = word.strip(punctuation)
                        if(not classificationFlag):
                            featureCount += 1
                            # Read in each feature after the title & initial feature
                            sepFeatures.append(key)
                        else:
                            classifications.append(key)
                # Add new line of features to the list of arrays
                features.append(sepFeatures)
        # Output completed notification to user
        outputLabel = ttk.Label(frm, text="Finished reading "+metaTxt.get(), padding=5).grid(column=2,row=10)
        startConsistency()
        print('-------------')
        print(features)
        print('-------------')
        print(features[0])
        print('-------------')
        print(titles)
        print('-------------')
        print(classifications)

        # j = 0
        # k = 0
        # data.append(titles)
        # data.append(features)
        # for title in titles:
        #     data[0][0] = title
        #     print(title)
        #     for feature in features:
        #         k +=1
        #         print(feature)
        #         data[j][k] = feature
        #     print(j, k)
        #     j += 1
        # print("--------")
        # print(data)
    except:
        fileFailed()

def create2DArray(rows, col):
    arr = []
    for i in range(rows):
        col = []
        for j in range(col):
            col.append(0)
        arr.append(col)

# Instantiate each value of the consistency starting at 1
def startConsistency():
    for title in titles:
        consistency = []
        i = 0
        if(title != "class"):
            for feature in features[i]:
                consistency.append(1)
                i += 1
            overallConsistency.append(consistency)

# Increment the number for each value when a line is accepted
def trainConsistency(word = ""):
    print(word)
    i = 0
    if(word != ""):
        if word in features[i]:
            overallConsistency[i][features[i].index(word)] += 1
            i += 1
    print(overallConsistency)

# Loading the training data
def loadTrain():
    try:
        if(titles and features):
            trainingFile = (trainTxt.get())
            outputLabel = ttk.Label(frm, text="Reading "+metaTxt.get()+"...", padding=5).grid(column=2,row=10)
            with open(trainingFile) as f:
                lines = f.readlines()
                for line in lines:
                    training = []
                    i = 0
                    for word in line.split(','):
                        if(word == "acc" or word == "unacc" or word == "good" or word == "vgood"):
                            for feature in training:
                                trainConsistency(feature)
                            correct += 1
                        elif(word == "unacc"):
                            failed += 1
                        else:
                            training.append(word.strip(punctuation))
                    print(training)
            # print(correct, failed)
            # print(overallConsistency)
            outputLabel = ttk.Label(frm, text="Finished training "+trainTxt.get(), padding=5).grid(column=2,row=10)
        else:
            wrongOrder()
    except:
        fileFailed()

# Loading the test files
def loadTest():
    try:
        if(titles and features):
            testFile = (testTxt.get())
            print(testFile)
            outputLabel = ttk.Label(frm, text="Reading "+metaTxt.get()+"...", padding=5).grid(column=2,row=10)
            with open(testFile) as f:
                lines = f.readlines()
                for line in lines:
                    for word in line.split(','):
                        testing.append(word.strip(punctuation))

            # print(testing)
            outputLabel = ttk.Label(frm, text="Finished testing "+testTxt.get(), padding=5).grid(column=2,row=10)
            outputLabel = ttk.Label(frm, text="Accuracy = " + accuracy(0.5), padding=5).grid(column=2,row=12)
        else:
            wrongOrder()
    except:
        fileFailed()

# Files that fail to load will run this window to notify the user
def fileFailed():
    fRoot = Tk()
    fFrame = ttk.Frame(fRoot, padding=20)
    fGrid = fFrame.grid()
    fLabel = ttk.Label(fFrame, text="File not found.", justify=CENTER, padding=3).grid(column=1, row=1)
    fBtn = ttk.Button(fFrame, text="Exit", command=fRoot.destroy).grid(column=3,row=3)

def wrongOrder():
    fRoot = Tk()
    fFrame = ttk.Frame(fRoot, padding=20)
    fGrid = fFrame.grid()
    fLabel = ttk.Label(fFrame, text="You need to read in the meta data then the training data, then the test data", justify=CENTER, padding=3).grid(column=1, row=1)
    fBtn = ttk.Button(fFrame, text="Exit", command=fRoot.destroy).grid(column=3,row=3)

def accuracy(x):
    if(x > 0.5):
        outputLabel = ttk.Label(frm, text="Solution: acc", padding=5).grid(column=2,row=11)
    else:
        outputLabel = ttk.Label(frm, text="Solution: unacc", padding=5).grid(column=2,row=11)
        return ("X/X")

def bayesClassifier():
    print('bayes')
# Create GUI root and frame
root = Tk()
frm = ttk.Frame(root, padding=20)
grid = frm.grid()
# helloLabel = ttk.Label(frm, text="Hello Universe!", justify=RIGHT, padding=10).grid(column=2, row=0)

# Create labels for each Entry
metaLabel = ttk.Label(frm, text="Enter .meta file").grid(column=2, row=1)
trainLabel = ttk.Label(frm, text="Enter .train file").grid(column=2, row=3)
testLabel = ttk.Label(frm, text="Enter .test file").grid(column=2, row=5)

# Create storing variable and each file entry case
metaTxt = StringVar()
trainTxt = StringVar()
testTxt = StringVar()
metaEntry = ttk.Entry(frm, textvariable=metaTxt, width=20).grid(column=2, row=2)
trainEntry = ttk.Entry(frm, textvariable=trainTxt, width=20).grid(column=2, row=4)
testEntry = ttk.Entry(frm, textvariable=testTxt, width=20).grid(column=2, row=6)

# Create buttons for each entry case
metaEntryBtn = ttk.Button(frm, text="Load", command=loadMeta).grid(column=3,row=2)
trainEntryBtn = ttk.Button(frm, text="Load", command=loadTrain).grid(column=3,row=4)
testEntryBtn = ttk.Button(frm, text="Load", command=loadTest).grid(column=3,row=6)

exitBtn = ttk.Button(frm, text="Quit", command=root.destroy).grid(column=7, row=6)

# symbols/commands to ignore
punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~\t\n\r\x0b\x0c'
# Run GUI
root.mainloop()
