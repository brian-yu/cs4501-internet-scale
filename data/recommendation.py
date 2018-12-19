from pyspark import SparkContext
import urllib.request
import urllib.parse
import json

def allPairs(a):
    pairs = []
    a = list(a)
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            pairs.append((min(a[i], a[j]), max(a[i], a[j])))
    return pairs

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

data = data.distinct()

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of its partition
itemsByUser = pairs.groupByKey()
items = itemsByUser.map(lambda pair: pair[1])
coclicks = items.flatMap(lambda item: allPairs(item))
coclicks = coclicks.map(lambda pair: (pair, 1))
count = coclicks.reduceByKey(lambda x,y: int(x)+int(y))
critical = count.filter(lambda x: x[1] >= 3).map(lambda x: x[0])
output = critical.collect()

for out in output:
    print("pair: {}".format(out))
    # write to models
    post_data = {'item1_id': int(out[0]), 'item2_id': int(out[1])}
    url = 'http://models-api:8000/api/v1/recommendations/create/'
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')

    req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if not resp['ok']:
        print('Something went wrong when writing to models')
    print(resp['result'])
        
print ("item recommendations done")

sc.stop()

'''
itemsByUser => 
        tp, [1,2,3,4,5]
        bob, [1,2,3,4]
items =>
        [1,2,3,4,5]
        [1,2,3,4]
coClicks (just map) =>
        [(1,2), (2,3) (1,3) ...]
        [(1,2), (2,3) (1,3) ...]

coclicks (with flatMap) =>
        (1,2)
        (2,3)
        (1,3)
        ...
        (1,2)
        (2,3)
        (1,3)
        ...
coclicks map =>
        (1,2), 1
        (2,3), 1
        (1,3), 1
        ...
        (1,2), 1
        (2,3), 1
        (1,3), 1

count =>
    (1,2), 2
    (2,3), 2
    (1,3), 2
'''