from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access.log", 2)

# tell each worker to split each line of it's partition
pairs = data.map(lambda line: line.split("\t"))
# re-layout the data to ignore the user id
pages = pairs.map(lambda pair: (pair[1], 1))
# shuffle the data so that each key is only on one worker
count = pages.reduceByKey(lambda x, y: int(x)+int(y))
# and then reduce all the values by adding them together

# bring the data back to the master node so we can print it out
output = count.collect()
for page_id, count in output:
    print("page_id %s count %d" % (page_id, count))
print("Popular items done")

sc.stop()
