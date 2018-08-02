import regression_tree
import copy
import numpy as np
import math

class GBRank(object):
    
    max_depth = 5
    feature_ratio = 0.7
    min_leaves = 2
    size_param = 0

    def __init__(self, data, iterations, margin, learning_ratio):
        """
        data is first col: query, final col: label
        """
        self.iterations = iterations
        self.margin = margin
        self.learning_ratio = learning_ratio

        # data add last col as the index
        # dataset is dict, key: query, val: feature...label, index
        print(len(data))
        dataset = dict()
        row_num = 0
        for line in data:
            line += [row_num]
            row_num += 1
            if line[0] not in dataset:
                dataset[line[0]] = list()
            dataset[line[0]].append(line[1:])

        self.testData = copy.deepcopy(data)

        for _, val in dataset.items():
            val.sort(key=lambda i: -i[-2])
        self.model_list = []
        self.train(dataset, data)

    def predict(self, dataset):
        prediction = [0 for i in range(len(dataset))]
        if len(self.model_list) == 0:
            return prediction
        for i in dataset:
            for model in self.model_list:
                prediction[i[-1]] += model.predict(i[1: -1])
            prediction[i[-1]] /= len(self.model_list)
        return prediction

    def train(self, dataset, data):
        for i in range(self.iterations):
            previous_prediction = self.predict(data)
            # print(previous_prediction)
            print(self.ndcg())
            next_dataset = list() # Only contains the inversed pairs
            for key, val in dataset.items():
                gradient = self.get_gradient(val, previous_prediction)
                for key, val in gradient.items():
                    # format source: features: label: count
                    next_row = copy.deepcopy(data[key])
                    next_row = next_row[1:-1]
                    next_row[-1] += self.learning_ratio * val[0] / val[1]
                    next_dataset.append(next_row) # first col is query, final col is index
            next_dataset = np.array(next_dataset)
            # print(next_dataset[0])
            # print(next_dataset)
            tree = regression_tree.fit(next_dataset, self.max_depth, self.feature_ratio, self.min_leaves, self.size_param)
            self.model_list.append(tree)
        
    
    def get_gradient(self, single_query_dataset, previous_prediction):

        # sort according to previous cumulative result
        # query_predict_dataset = copy.deepcopy(single_query_dataset)
        # query_predict_dataset.sort(lambda x, y: cmp(previous_prediction[x[-1]], previous_prediction[y[-1]]), reverse=True)
        
        # gradient should store [index, gradientSum, times]
        gradient = dict()
        for i in range(len(single_query_dataset)):
            idx_i = single_query_dataset[i][-1]            
            val_i = previous_prediction[idx_i]
            for j in range(i + 1, len(single_query_dataset)):
                idx_j = single_query_dataset[j][-1]
                val_j = previous_prediction[idx_j]
                # check whether i and j has different label
                if single_query_dataset[i][-2] == single_query_dataset[j][-2]:
                    continue
                if val_i - val_j <= self.margin:
                    if idx_i not in gradient:
                        gradient[idx_i] = [0, 0]
                    gradient[idx_i][0] += val_j - val_i + self.margin
                    gradient[idx_i][1] += 1
                    if idx_j not in gradient:
                        gradient[idx_j] = [0, 0]
                    gradient[idx_j][0] -= val_j - val_i + self.margin
                    gradient[idx_j][1] += 1
        return gradient
    
    def ndcg(self):
        data = self.testData
        dataset = dict()
        for line in data:
            if line[0] not in dataset:
                dataset[line[0]] = list()
            dataset[line[0]].append(line[1:])
        
        prediction = self.predict(data)
        sum_ndcg = 0
        for _, val in dataset.items():
            val.sort(key=lambda i: -prediction[i[-1]])
            dcg = 0
            for i in range(len(val)):
                dcg += 2**val[i][-2] / math.log2(i + 2)
            val.sort(key=lambda i: -i[-2])
            idcg = 0
            for i in range(len(val)):
                idcg += 2**val[i][-2] / math.log2(i + 2)
            sum_ndcg += dcg / idcg
        return sum_ndcg / len(dataset)

def read_file(filename):
    """
    special function to read test file
    """
    data = list()
    with open(filename, mode='r', encoding='gbk', errors='ignore') as f:
        for line in f.readlines()[1:100]:
            row = line.split('\t')
            line_data = [row[1]] + [float(i) for i in row[2: -1]] + [float(row[0])]
            # data format source: features: label
            data.append(line_data)
    return data

def read_IPS_file(filename, nlines):
    data = list()
    from itertools import islice
    with open(filename, 'r') as f:
        for line in islice(f, nlines):
            row = line.split(',')
            line_data = [row[1]] + [float(i) for i in row[3: -1]] + [float(row[-1])]
            data.append(line_data)
    return data

if __name__ == '__main__':

    # data = read_file('./testdata.tsv')
    data = read_IPS_file('C:/Users/t-qixu/Desktop/ActiveFeaturesV2.csv', 10000)

    gb = GBRank(data, 10, 0.3, 1)