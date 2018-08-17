# coding=utf-8

import numpy
import random


def get_random_index(len, ratio):
    return random.sample(range(len), int(ratio * len))


class TreeNode(object):
    def __init__(self, feature_index, split_point, depth, dataset):
        self.feature_index = feature_index
        self.split_point = split_point
        self.depth = depth
        self.left = None
        self.right = None
        self.is_leave = False
        self.value = None
        self.dataset = dataset
        


class Tree(object):
    def __init__(self, dataset, max_depth, feature_ratio, min_leaves, size_param, emphasize=[]):
        self.max_depth = max_depth
        self.feature_ratio = feature_ratio
        self.min_leaves = min_leaves
        self.size_param = size_param
        self.feature_weight = [0 for i in range(dataset[0].size - 1)]   
        self.emphasize = emphasize     
        self.root = self.create_tree(dataset)

    def predict(self, data, node=None):
        if node is None:
            node = self.root
        if node.is_leave:
            return node.value
        index = node.feature_index
        if type(data[index]) == type(""):
            print(data)
        if data[index] < node.split_point:
            node = node.left
        else:
            node = node.right
        return self.predict(data, node)

    def create_tree(self, dataset, depth=0):

        feature_index, mean, best_lt_dataset, best_gt_dataset = self.choose_feature(dataset, self.feature_ratio)
        node = TreeNode(feature_index, mean, depth, dataset)

        if depth == self.max_depth \
                or best_lt_dataset is None \
                or best_gt_dataset is None \
                or dataset.size <= self.min_leaves:
            node.is_leave = True
            node.value = dataset[:, -1].mean(0)
            return node

        node.left = self.create_tree(best_lt_dataset, depth + 1)
        node.right = self.create_tree(best_gt_dataset, depth + 1)
        return node

    def choose_feature(self, dataset, ratio):
        min_mean = None
        min_var = numpy.inf
        best_lt_dataset = None
        best_gt_dataset = None
        feature_index = None

        for index in get_random_index(dataset[0].size - 1, ratio):
            mean = dataset[:, index].mean(0)
            gt_dataset = dataset[dataset[:, index] > mean, :]
            lt_dataset = dataset[dataset[:, index] <= mean, :]

            if gt_dataset[:, 0].size == 0 or lt_dataset[:, 0].size == 0:
                continue

            var = lt_dataset[:, -1].var() + gt_dataset[:, -1].var()
            if len(self.emphasize) != 0:
                var *= self.emphasize[index]
            if var < min_var:
                min_mean = mean
                feature_index = index
                min_var = var
                best_gt_dataset = gt_dataset
                best_lt_dataset = lt_dataset
        if feature_index != None:
            self.feature_weight[feature_index] += 1
        return feature_index, min_mean, best_lt_dataset, best_gt_dataset


def fit(dataset, max_depth, feature_ratio, min_leaves, size_param, emphasize):
    """
    :param dataset: 2D numpy array, where the last column is label
    :return: a trained model using regression tree
    """
    tree = Tree(dataset, max_depth, feature_ratio, min_leaves, size_param, emphasize)
    return tree


def accuracy(tree, dataset):
    right = 0
    for data in dataset:
        res = tree.predict(data)
        if abs(res - data[-1]) <= 0.5:
            right += 1
    return right / dataset[:, 0].size


if __name__ == '__main__':
    file = 'Jain_373_2.txt'
    dataset = [[float(j) for j in i.rstrip().split(',')] for i in open(file).readlines()]
    dataset = numpy.array(dataset)
    tree = fit(dataset, 5, 1, 1, 0, [])
    print(accuracy(tree, dataset))
