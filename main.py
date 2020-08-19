import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
nltk.download('punkt')

import numpy
import tflearn
import pickle
import tensorflow
import random
import json
import discord

token = "NzIwOTAyMzE1MTk1NzYwNjYw.XuMvow.tS-3plkntnm7ymXeIPNB-SopAtc"

client = discord.Client()

with open("SpaceCenterData.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        wordList, listOfHeaders, modelTrain, modelOutput = pickle.load(f)
except:
    wordList = [] 
    listOfHeaders = []
    stemmedList = []
    keyList = []

    for category in data["categories"]:
        for question in category["questions"]:
            rawWords = nltk.word_tokenize(question)
            wordList.extend(rawWords)
            stemmedList.append(rawWords)
            keyList.append(category["key"])

        if category["key"] not in listOfHeaders:
            listOfHeaders.append(category["key"])

    wordList = [stemmer.stem(word.lower()) for word in wordList if word != "?"]
    wordList = sorted(list(set(wordList)))

    listOfHeaders = sorted(listOfHeaders)

    modelTrain = []
    modelOutput = []

    outputNoMatch = [0 for _ in range(len(listOfHeaders))]

    for x, doc in enumerate(stemmedList):
        sack = []

        rawWords = [stemmer.stem(word.lower()) for word in doc]

        for word in wordList:
            if word in rawWords:
                sack.append(1)
            else:
                sack.append(0)

        outputCategory = outputNoMatch[:]
        outputCategory[listOfHeaders.index(keyList[x])] = 1

        modelTrain.append(sack)
        modelOutput.append(outputCategory)

    modelTrain = numpy.array(modelTrain)
    modelOutput = numpy.array(modelOutput)

    with open("data.pickle", "wb") as f:
        pickle.dump((wordList, listOfHeaders, modelTrain, modelOutput), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(modelTrain[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(modelOutput[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(modelTrain, modelOutput, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

def wordSack(s, wordList):
    sack = [0 for _ in range(len(wordList))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, word in enumerate(wordList):
            if word == se:
                sack[i] = 1
    return numpy.array(sack)

@client.event
async def on_message(message):
    if message.author.id != 720902315195760660:
        results = model.predict([wordSack(message.content, wordList)])[0]
        results_index = numpy.argmax(results)
        key = listOfHeaders[results_index]
        if results[results_index] > 0.9:
            for tg in data["categories"]:
                if tg['key'] == key:
                    responses = tg['responses']
            await message.channel.send(responses[0])
        else:
            await message.channel.send("I did not catch that. However, for the most up to date information, please visit https://spacecenter.org/reopening/")    
print("\n-------ChatBot Online-------")
client.run(token)
