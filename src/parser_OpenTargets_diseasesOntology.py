from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

import pandas as pd
from os.path import join
import os
import networkx as nx
from tqdm import tqdm

def isNaN(num):
    return num != num


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
# ~ dis.printSchema()


disSelect = (dis
 .select("id",
         "name",
         # ~ "code",
         "children",
         "descendants",
         "ancestors",
         "parents",
         # ~ "dbXRefs",
         # ~ "synonyms",
         # ~ "description"

         )
 )


# Convert to a Pandas Dataframe
ent = disSelect.toPandas()


G = nx.MultiDiGraph()

cl_prop = ["id","name"]
cl_rel = ["id",
          "children",
         "descendants",
         "ancestors",
         "parents"]


for ind,rw in tqdm(ent[cl_prop].iterrows()):
    pr = dict(rw)
    pr = {k:v for k,v in pr.items() if not isNaN(v)}
    pr["labels"]=ENTITY
    G.add_node(rw["id"],**pr)

if len(cl_rel)>1:
    for ind,rw in tqdm(ent[cl_rel].iterrows()):
        pr = dict(rw)
        pr.pop("id")
        # ~ pr = {k.split(":")[1]:v for k,v in pr.items()}
        for k,v in pr.items():
            if not isNaN(v):
                if not isinstance(v,list):
                    v = [v]
                ed = [(rw["id"],u) for u in v]
                G.add_edges_from(ed,label=k)   

# ~ if len(cl_ler)>1:
    # ~ for ind,rw in tqdm(ent[cl_ler].iterrows()):
        # ~ pr = dict(rw)
        # ~ pr.pop("ID")
        # ~ pr = {k.split(":")[1]:v for k,v in pr.items()}
        # ~ for k,v in pr.items():
            # ~ if not isNaN(v):
                # ~ if not isinstance(v,list):
                    # ~ v = [v]
                # ~ ed = [(u,rw["ID"]) for u in v]
                # ~ G.add_edges_from(ed,label=k) 









# ~ col_u = {
    # ~ "id":"ID",
    # ~ "name":"Name",
    # ~ "synonyms":"Synonyms",
    # ~ "dbXRefs":"xref"
# ~ }

# ~ df = df.rename(columns=col_u)

# ~ df.to_csv(join(path_out,f"{ENTITY}.csv"),index=False)
