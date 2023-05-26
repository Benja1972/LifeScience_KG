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
ENTITY_FLD = "molecule"
ENTITY = "Compound"
path_out = "../data/PROCESSED/nodes"

frec = join(PATH,ENTITY_FLD)


spark = (SparkSession.builder.master('local[*]').getOrCreate())

dis = spark.read.parquet(frec)
dis.printSchema()

disSelect = (dis
 .select("id",
         "name",
         "drugType",
         "maximumClinicalTrialPhase",
         "isApproved",
         "tradeNames",
         "synonyms",
         "crossReferences",
         "linkedTargets",
         "linkedDiseases",
         "description"
         )
 )


# Convert to a Pandas Dataframe
df = disSelect.toPandas()


col_u = {
    "id":"ID",
    "name":"Name",
    "synonyms":"Synonyms",
    "crossReferences":"xref"
}

df = df.rename(columns=col_u)


def map_linked(l):
    mp=[]
    if l is not None :
        mp = list(l[0])

    return mp



df["REL:targets"] = df["linkedTargets"].apply(lambda x: map_linked(x))
df["REL:has_effect_on"] = df["linkedDiseases"].apply(lambda x: map_linked(x))
df.drop(["linkedTargets","linkedDiseases"],inplace=True,axis=1)


# Mapping to PubChem
f_pub = "../data/xRefs/CID-CHEMBL"
pub = pd.read_csv(f_pub, index_col=1,sep = "\t",names=["PUBCHEM","CHEMBL"])
pub["PUBCHEM"] =pub["PUBCHEM"].apply(lambda x: "Pubchem.Compound:"+str(x))
ch = df["ID"].tolist()
pub = pub[pub.index.isin(ch)]

pub = pub.groupby(pub.index).agg({"PUBCHEM":lambda x: x.unique().tolist()})
pubin = list(pub.index)


def map_pubch(l):
    mp = []
    if l in pubin:
        mp = pub.loc[l]["PUBCHEM"]
        # ~ if isinstance(mp,str):
            # ~ mp = [mp] 
        # ~ else:
            # ~ mp = list(mp)

    return mp

df["REL:same_as"] = df["ID"].apply(lambda x: map_pubch(x))


df.to_csv(join(path_out,f"{ENTITY}:OT.csv"),index=False)
