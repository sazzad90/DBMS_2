from collections import defaultdict
import csv
import itertools

import k as k


# Reads Csv File
def read_csv(file_path):
    dataList = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for i, row in enumerate(csvreader):
            row_data = []
            i_data = []
            for j, val in enumerate(row):
                if j == 0:
                    row_data.append(val)
                    continue

                if val != '':
                    i_data.append(val)

            row_data.append(i_data)
            dataList.append(row_data)

    return dataList


def calculateConfidence(itemsList, dataList):
    count = 0
    for item in dataList:
        mSet = set(item[1])
        cSet = set(itemsList)

        if cSet.issubset(mSet):
            count += 1
    return count


def confidence(transactionData):
    inputStr = input('Enter transactions: ')
    inputStr = inputStr.replace(' ', '')

    parseInputStr = inputStr.split("->")
    leftItems = parseInputStr[0].split(",")
    rightItems = parseInputStr[1].split(",")

    denominator = calculateConfidence(leftItems, transactionData)
    numerator = calculateConfidence(leftItems + rightItems, transactionData)

    confidenceValue = 0
    if numerator == 0:
        return 0
    else:
        confidenceValue = (numerator / denominator) * 100.0
        return confidenceValue


if __name__ == "__main__":

    min_support = 2
    dataList = read_csv("input.csv")

    frequencyList = defaultdict(int)
    for items in dataList:
        for item in items[1]:
            frequencyList[item] += 1
    minSupportList = dict((item, support)
                          for item, support in frequencyList.items()
                          if support >= min_support)

    for item in minSupportList:
        print(item, frequencyList[item])
    print("\n")

    combinationCount = 2
    while True:
        frequencyList = defaultdict(int)
        for items in dataList:
            item = set(items[1])
            for subset in itertools.combinations(item, combinationCount):
                frequencyList[subset] += 1
        minSupportList = dict((item, support)
                              for item, support in frequencyList.items()
                              if support >= min_support)
        if len(minSupportList) == 0:
            break

        combinationCount += 1

        for item in minSupportList:
            print(item, frequencyList[item])
        print("\n")



    print("\nConfidence: ", confidence(dataList), "%")
