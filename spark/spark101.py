import pyspark
import pandas as pd
import numpy as np

spark = pyspark.sql.SparkSession.builder.getOrCreate()

languages = pd.DataFrame({'language': ['ruby', 'python', 'java', 'scala', 'haskell', 'go', 'clojure', 'c++']})

df = spark.createDataFrame(languages)
df.printSchema() # shows schema
