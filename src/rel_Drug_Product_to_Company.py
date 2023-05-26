
# ~ from rdflib import Graph
import numpy as np

# ~ import networkx as nx
import pandas as pd
from os.path import join
from tqdm import tqdm
import os
import hashlib

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



# ~ import sys
# ~ sys.path.append("/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/src/")

# ~ from BioOntoTools import *

def isNaN(num):
    return num != num








NSAMPLE = 0

PATH ="../data/FDA/"
ENTITY1 ="Company"
ENTITY2 ="Drug_product"

PATH_ENT1 =join(PATH,f"{ENTITY1}/Processed/{ENTITY1}.csv")
PATH_ENT2 =join(PATH,f"{ENTITY2}/Processed/{ENTITY2}.csv")




drug = pd.read_csv(PATH_ENT2)
comp = pd.read_csv(PATH_ENT1)
if NSAMPLE >0:
    drug = drug.sample(NSAMPLE)
    comp = comp.sample(NSAMPLE)



import ast


cm = drug["Company"].unique()
cm = [ast.literal_eval(c) for c in cm]
cm = [c for m in cm for c in m]



comp["name"] = comp["Name"].apply(str.lower)



mc = {c:comp[comp["name"]==c.lower()]["ID"].tolist() for c in cm}
alpc =  {"ALP:"+hashlib.md5(k.encode('utf-8')).hexdigest():k for k,v in mc.items() if len(v)==0 }
mc =  {k:["ALP:"+hashlib.md5(k.encode('utf-8')).hexdigest()] if len(v)==0 else v for k,v in mc.items()}

# Unlisted companies for record linkage 
ENTITY = "Company"
df = pd.DataFrame.from_dict(alpc,orient="index",columns=["Name"])
df["ID"] = df.index
path_out = "../data/ALP_ENTITY"
df[["ID","Name"]].to_csv(join(path_out,f"ALP_{ENTITY}.csv"),index=False)


def map_comp(ls):
    mls = ast.literal_eval(ls)
    if len(ls)>0:
        mls = [mc[c]  for c in mls if c in mc.keys()]
        mls = [c for m in mls for c in m]
    else:
        mls=[]
    return mls

# ~ drug["LER:manufactures"] = drug["Company"].apply(map_comp)
# ~ drug.to_csv(PATH_ENT2,index=False)

