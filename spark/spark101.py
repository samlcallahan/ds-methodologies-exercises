import pyspark
import pandas as pd
import numpy as np
import pyspark.sql.functions as F
from pydataset import data


spark = pyspark.sql.SparkSession.builder.getOrCreate()

languages = pd.DataFrame({'language': ['ruby', 'python', 'java', 'scala', 'haskell', 'go', 'clojure', 'c++']})

df = spark.createDataFrame(languages)
df.printSchema() # shows schema
print((df.count(), len(df.columns)))
df.show(5)

mpg = data('mpg')
mpg = spark.createDataFrame(mpg)

mpg.select(F.concat(F.lit('The '), mpg.year, F.lit(' '), mpg.manufacturer, F.lit(' '), mpg.model, F.lit(' has a '), mpg.cyl, F.lit(' cylinder engine.'))).show(truncate=False)

mpg.select(F.when(mpg.trans.startswith('auto'), 'auto').otherwise('manual')).show()

tips = data('tips')
tips = spark.createDataFrame(tips)

tips.filter(tips.smoker == 'Yes').count() / tips.count()

tips.percent = F.round(tips.tip / tips.total_bill, 2)

tips.groupBy(tips.sex, tips.smoker).agg(F.avg(tips.percent)).show()

