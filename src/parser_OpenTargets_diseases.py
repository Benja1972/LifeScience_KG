from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

import pandas as pd
from os.path import join
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


PATH ="../data/OpenTargets"
ENTITY_FLD = "diseases"
ENTITY = "Disease"
path_out = "../data/PROCESSED"

frec = join(PATH,ENTITY_FLD)


spark = (SparkSession.builder.master('local[*]').getOrCreate())

dis = spark.read.parquet(frec)
dis.printSchema()


disSelect = (dis
 .select("id",
         "name",
         "code",
         "dbXRefs",
         "synonyms",
         "description"
         # ~ F.explode("clinicalSignificances").alias("cs"),
         )
 )


# Convert to a Pandas Dataframe
df = disSelect.toPandas()


col_u = {
    "id":"ID",
    "name":"Name",
    "synonyms":"Synonyms",
    "dbXRefs":"xref"
}

df = df.rename(columns=col_u)

df.to_csv(join(path_out,f"{ENTITY}.csv"),index=False)
