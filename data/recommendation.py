from pyspark import SparkContext

def allPairs(a):
	pairs = []
	a = list(a)
	for i in range(len(a)):
		for j in range(i+1, len(a)):
			pairs.append((min(a[i], a[j]), max(a[i], a[j])))
	return pairs

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/test.log", 2)     # each worker loads a piece of the data file

data = data.distinct()

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
itemsByUser = pairs.groupByKey()
items = itemsByUser.map(lambda pair: pair[1])
coclicks = items.flatMap(lambda item: allPairs(item))
coclicks = coclicks.map(lambda pair: (pair, 1))
count = coclicks.reduceByKey(lambda x,y: int(x)+int(y))
critical = count.filter(lambda x: x[1] >= 3).map(lambda x: x[0])
output = critical.collect()

for out in output:
	print("pair: {}".format(out))

print ("item recommendations done")

# print(counts)

# criticalMass = {k: counts[k] for k in counts if counts[k] >= 3}

sc.stop()