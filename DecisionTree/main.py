import pprint
import csv
import math
from sklearn.model_selection import train_test_split

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


def predict(row, tree):
    if isinstance(tree, str):  # leaf node
        return tree
    attribute = list(tree.keys())[0]

    value = row[attribute]
    subtree = tree[attribute].get(value)  # returns None value if value not seen during training
    if subtree is None:
        return None
    return predict(row, subtree)



# main #

data = read_data('car.csv')

# Split data into training and testing sets
train_data, test_data = train_test_split(data, test_size=0.1)

attributes = set(range(len(data[0]) - 1))
tree = build_tree(train_data, attributes)

pprint.pprint(tree)


#  test section
correct_predictions = 0
for row in test_data:
    predicted_label = predict(row, tree)
    true_label = row[-1]
    if predicted_label == true_label:
        correct_predictions += 1

accuracy = correct_predictions / len(test_data)
print(f"Accuracy on test data: {accuracy}")
