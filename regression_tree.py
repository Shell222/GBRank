# coding=utf-8

import numpy
import random

def get_random_index(len, ratio):
    """Get a randomly sample size of ratio * len from 0 to len

    Arguments:
        len {int} -- indicate the length
        ratio {double} -- ratio of picking up numbers

    Returns:
        list -- list of sampled data
    """
    return random.sample(range(len), int(ratio * len))


class TreeNode(object):
    """TreeNode obj for the regression tree
    """
    def __init__(self, feature_index, split_point, depth, dataset):
        """Constructor for tree node
        
        Arguments:
            feature_index {int} -- the index that is currently being splitted on this ndoe
            split_point {double} -- the value of split 
            depth {int} -- indicate the tree depth
            dataset {list} -- the data that the current node is splitting
        """
        self.feature_index = feature_index
        self.split_point = split_point
        self.depth = depth
        self.left = None
        self.right = None
        self.is_leave = False
        self.value = None
        self.dataset = dataset
        


class Tree(object):
    """A Regression tree object
    """

    def __init__(self, dataset, max_depth, feature_ratio, min_leaves, size_param, emphasize=[]):
        """Constructor
        
        Arguments:
            dataset {numpy.array} -- Original data set where last col is label
            max_depth {int} -- Parameter for prunning
            feature_ratio {double} -- Parameter of randomly sampling features
            min_leaves {int} -- Min leaves for stop splitting
            size_param {int} -- No usage
        
        Keyword Arguments:
            emphasize {list} -- Parameter for the emphasize for each feature. 1 means no emphasize, the smaller, the more weight (default: {[]})
        """

        self.max_depth = max_depth
        self.feature_ratio = feature_ratio
        self.min_leaves = min_leaves
        self.size_param = size_param
        self.feature_weight = [0 for i in range(dataset[0].size - 1)]   
        self.emphasize = emphasize     
        # start create tree
        self.root = self.create_tree(dataset)

    def predict(self, data, node=None):
        """After initialization, call this function to predict one line of data
        
        Arguments:
            data {list} -- data to be predicted
        
        Keyword Arguments:
            node {TreeNode} -- Current iterating node (default: {None})
        
        Returns:
            double -- result of prediction
        """

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
        """Recursive call to make a regression tree
        
        Arguments:
            dataset {list} -- current splitting dataset
        
        Keyword Arguments:
            depth {int} -- current depth (default: {0})
        
        Returns:
            TreeNode -- splitting result
        """

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
        """Choose feature for the current splitting data set
        
        Arguments:
            dataset {list} -- current splitted dataset
            ratio {double} -- ratio of sampling feature
        
        Returns:
            feature index -- the chosen index
            mean value -- the split point of the chosen feature
            best larger dataset & best less dataset ---  the spliitd dataset
        """

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
    """
    :param dataset: 2D numpy array, where the last column is label
    
    :return: a trained model using regression tree
    """

def fit(dataset, max_depth, feature_ratio, min_leaves, size_param, emphasize):
    """Function to tain data into a regression tree 
    
    Arguments:
        dataset {numpy.array} -- 2D numpy array, where the last column is label
        max_depth {int} -- prunning parameter
        feature_ratio {double} -- Parameter of randomly sampling features
        min_leaves {int} -- [description]
        size_param {int} -- No usage
        emphasize {list} -- Parameter for the emphasize for each feature,range (0,1]. 1 means no emphasize, the smaller, the more weight
    
    Returns:
        Tree -- a trained model using regression tree
    """


    tree = Tree(dataset, max_depth, feature_ratio, min_leaves, size_param, emphasize)
    return tree


def accuracy(tree, dataset):
    """Function to calculate the accuracy of a regressiontree
    
    Arguments:
        tree {Tree} -- Trained model
        dataset {list} -- Testing dataset
    
    Returns:
        double -- accuracy
    """

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
