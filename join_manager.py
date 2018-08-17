from itertools import islice
import operator as op

if __name__ == '__main__':
    manager = dict()
    with open('../report_hierarchy.csv', 'r') as f:
        for line in f.readlines():
            data = line.split(',')
            manager[data[0]] = data[1][0:-1]

    joined = open('../joined.csv', 'w')
    with open('../ActiveFeaturesV2 MS.csv', 'r') as f:
        for line in f.readlines():
        # for line in islice(f, 1000):
            data = line[0:-1].split(',')
            if data[1] in manager and manager[data[1]] == data[2]:
                data.insert(-1, "1")
                data[-1] = "4"
            else:
                data.insert(-1, "0")
            joined.write(','.join(data))
            joined.write('\n')
    joined.close()
