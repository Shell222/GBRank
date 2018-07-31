
import regression_tree
import copy

class GBRank(object):
    
    max_depth = 4
    feature_ratio = 0.7
    min_leaves = 50 
    size_param = 0

    def __init__(self, data, iterations, margin, data_size, learning_ratio):
        """
        data is first col: query, final col: label
        """
        self.iterations = iterations
        self.margin = margin
        self.learning_ratio = learning_ratio

        # data add last col as the index
        # dataset is dict, key: query, val: feature...label, index
        dataset = dict()
        row_num = 0
        for line in data:
            line += [row_num]
            row_num += 1
            if line[0] not in dataset:
                dataset[line[0]] = list()
            dataset[line[0]].append(line[1:])

        for _, val in dataset.items():
            val.sort(key=lambda i:i[-2], reversed=True)

        self.model_list = self.train(dataset, data)

    def predict(self, dataset):
        prediction = [0 for i in range(len(dataset))]
        if len(self.model_list) == 0:
            return prediction
        for i in dataset:
            for model in self.model_list:
                previous_prediction[i[-1]] += model.predict(i[0: -2])
            previous_prediction[i[-1]] /= len(self.model_list)
        return prediction

    def train(self, dataset, data):
        model_list = list()
        for i in range(self.iterations):
            previous_prediction = self.predict(data)
            next_dataset = list() # Only contains the inversed pairs
            for key, val in dataset.items():
                gradient = self.get_gradient(val, previous_prediction)
                for key, val in gradient.items():
                    next_row = copy.deepcopy(data[key])
                    next_row[-2] += self.learning_ratio * val[0] / val[1]
                    next_dataset.append(next_row[1: -1]) # first col is query, final col is index
            tree = regression_tree.fit(next_dataset, self.max_depth, self.feature_ratio, self.min_leaves, self.size_param)
            model_list.append(tree)
        return model_list
    
    def get_gradient(self, single_query_dataset, previous_prediction):

        # sort according to previous cumulative result
        # query_predict_dataset = copy.deepcopy(single_query_dataset)
        # query_predict_dataset.sort(lambda x, y: cmp(previous_prediction[x[-1]], previous_prediction[y[-1]]), reverse=True)
        
        # gradient should store [index, gradientSum, times]
        gradient = dict()
        for i in len(single_query_dataset):
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
                    gradient[idx_j] -= val_j - val_i + self.margin
                    gradient[idx_j][1] += 1
        return gradient

def read_file(filename):
    """
    special function to read test file
    """
    data = list()
    first_line = True
    with open(filename) as f:
        for line in f.readlines():
            if first_line:
                first_line = False
                continue
            row = line.split('\t')
            line_data = [row[1]] + [float(i) for i in row[2: -1]] + [row[0]]
            data.append(line_data)
    return data

if __name__ == '__main__':
    pass