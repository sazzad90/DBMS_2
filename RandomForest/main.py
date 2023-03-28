
import pprint
import csv
import math
from sklearn.model_selection import train_test_split
import random
from sklearn.svm._libsvm import predict

def read_data(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    return data

def entropy(data):
    counts = {}
    for row in data:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    entropy = 0
    for label in counts:
        p = counts[label] / len(data)
        entropy -= p * math.log2(p)
    return entropy


def split_data(data, attribute, value):

    split_data = []
    for row in data:
        if row[attribute] == value:
            split_data.append(row)
    return split_data


def information_gain(data, attribute):
    total_entropy = entropy(data)
    attribute_values = set(row[attribute] for row in data)
    subset_entropy = 0
    for value in attribute_values:
        subset = split_data(data, attribute, value)
        subset_entropy += len(subset) / len(data) * entropy(subset)
    return total_entropy - subset_entropy


def build_tree(data, attributes):
    # If all examples have the same label, return a leaf node with that label
    labels = set(row[-1] for row in data)

    if len(labels) == 1:
        return labels.pop()
    # If no attributes are left, return a leaf node with the majority label
    if not attributes:
        label_counts = {}
        for row in data:
            label = row[-1]
            if label not in label_counts:
                label_counts[label] = 0
            label_counts[label] += 1
        return max(label_counts, key=label_counts.get)
    # Otherwise, choose the best attribute to split on and create a subtree for each value

    best_attribute = None
    max_information_gain = -1

    for attribute in attributes:
        current_information_gain = information_gain(data, attribute)
        if current_information_gain > max_information_gain:
            max_information_gain = current_information_gain
            best_attribute = attribute


    tree = {best_attribute: {}}
    attributes.remove(best_attribute)

    unique_values = set()
    for row in data:
        value = row[best_attribute]
        unique_values.add(value)

    for value in unique_values:
        subset = split_data(data, best_attribute, value)
        subtree = build_tree(subset, attributes.copy())
        tree[best_attribute][value] = subtree
    return tree


def build_forest(data, num_trees, num_attributes):
    forest = []
    for i in range(num_trees):
        # subset = random.sample(data, int(0.8*len(data)))

        random.seed(42)  # set a seed for reproducibility
        subset = random.sample(list(data), int(0.8 * len(data)))

        attributes = random.sample(list(range(len(data[0]) - 1)), num_attributes)

        tree = build_tree(subset, attributes)
        forest.append(tree)
    return forest


def predict(row, tree):
    if isinstance(tree, str):
        return tree
    else:
        attribute = list(tree.keys())[0]
        if row[attribute] in tree[attribute]:
            subtree = tree[attribute][row[attribute]]
            return predict(row, subtree)
        else:
            return None

def predict_forest(row, forest):
    predictions = {}
    for tree in forest:
        label = predict(row, tree)
        if label in predictions:
            predictions[label] += 1
        else:
            predictions[label] = 1
    return max(predictions, key=predictions.get)



# main #
data = read_data('car.csv')

train_data, test_data = train_test_split(data, test_size=0.1)


forest = build_forest(train_data,20, 6)

# test section
correct_predictions = 0
for row in test_data:
    predicted_label = predict_forest(row, forest)
    true_label = row[-1]
    if predicted_label == true_label:
        correct_predictions += 1

accuracy = correct_predictions / len(test_data)
print(f"Accuracy on test data: {accuracy}")