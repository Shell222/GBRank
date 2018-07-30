#coding=utf-8

import numpy
import json
import random
import sklearn

def get_random_index(len, ratio):
    return random.sample(range(len), int(ratio * len));

class TreeNode(object):
    def __init__(self, feature_index, split_point, depth):
        self.feature_index = feature_index
        self.split_point = split_point
        self.depth = depth
        self.left = None
        self.right = None
        self.is_leave = False
        self.value = None


class Tree(object):
    def __init__(self, dataset, max_depth, feature_ratio, min_leaves, size_param):
        self.max_depth = max_depth
        self.feature_ratio = feature_ratio
        self.min_leaves = min_leaves
        self.size_param = size_param
        self.root = self.create_tree(dataset)

    def predict(self, data, node):
        if node.is_leave:
            return node.val
        index = node.index
        if data[index] > node.split_point:
            node = node.left
        else:
            node = node.right
        return self.predict(data, node)

    def create_tree(self, dataset, depth = 0):

        feature_index, mean, best_lt_dataset, best_gt_dataset = self.choose_feature(dataset, self.feature_ratio)
        node = TreeNode(feature_index, mean, depth);

        if depth == self.max_depth \
            or best_lt_dataset is None \
            or best_gt_dataset is None \
            or best_lt_dataset.size == 0 \
            or best_gt_dataset.size == 0:
            node.is_leave = True
            node.value = dataset[: -1].mean(0)
            return node

        node.left = self.create_tree(best_lt_dataset, depth + 1)
        node.right = self.create_tree(best_gt_dataset, depth + 1)
        return node

    def choose_feature(self, dataset, ratio):
        mean = dataset[:, :-1].mean(0)
        min_var = numpy.inf
        best_lt_dataset = None
        best_gt_dataset = None
        feature_index = None

        for index in get_random_index(dataset[0].size - 1, ratio):

            gt_dataset = dataset[ dataset[:, index] > mean[index], :]
            lt_dataset = dataset[ dataset[:, index] <= mean[index], :]

            if gt_dataset.size == 0 or lt_dataset.size == 0:
                continue

            var = lt_dataset[:,-1].var() + gt_dataset[:,-1].var()
            if var < min_var:
                feature_index = index
                min_var = var
                best_gt_dataset = gt_dataset
                best_lt_dataset = lt_dataset

        return feature_index, mean[feature_index], best_lt_dataset, best_gt_dataset


def fit(dataset, max_depth, feature_ratio, min_leaves, size_param):
    """
    :param dataset: 2D numpy array, where the last column is label
    :return: a trained model using regression tree
    """
    tree = Tree(dataset, max_depth, feature_ratio, min_leaves, size_param)
    return tree

if __name__ == '__main__':
