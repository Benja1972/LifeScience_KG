import numpy as np

import networkx as nx
import pandas as pd
from os.path import join
from tqdm import tqdm
import os
import ast
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import glob


def delist_batch(H):
    for nd in H.nodes:
        atr = dict(H.nodes[nd])
        atr = {k:v for k,v in atr.items() if isinstance(v,list)}
        if len(atr)>0:
            for at in atr.keys():
                H.nodes[nd][at] = f"{H.nodes[nd][at]}"
    return H



# ~ import sys
# ~ sys.path.append("/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/src/")

# ~ from BioOntoTools import *

def isNaN(num):
    return num != num


def table2graph(path_ent):
    ENT = os.path.basename(path_ent).split(".")[0]
    ENT = ENT.split(":")[0]
    print(ENT)
    ent = pd.read_csv(path_ent)
    ## TODO
    if ENT != "Gene":
        ent = ent.applymap(lambda x: ast.literal_eval(x) if isinstance(x,str) and x.startswith("[") and x.endswith("]") else x)


    clms = list(ent.columns)

    cl_prop = [e for e in clms if not e.startswith("REL:") and not e.startswith("LER:")]
    cl_rel = ["ID"]+[e for e in clms if e.startswith("REL:")]
    cl_ler = ["ID"]+[e for e in clms if e.startswith("LER:")]

    
    G = nx.DiGraph()
    for ind,rw in tqdm(ent[cl_prop].iterrows()):
        pr = dict(rw)
        pr = {k:v for k,v in pr.items() if not isNaN(v)}
        pr["labels"]=ENT
        G.add_node(rw["ID"],**pr)

    if len(cl_rel)>1:
        for ind,rw in tqdm(ent[cl_rel].iterrows()):
            pr = dict(rw)
            pr.pop("ID")
            pr = {k.split(":")[1]:v for k,v in pr.items()}
            for k,v in pr.items():
                if not isNaN(v):
                    if not isinstance(v,list):
                        v = [v]
                    ed = [(rw["ID"],u) for u in v]
                    G.add_edges_from(ed,label=k)   

    if len(cl_ler)>1:
        for ind,rw in tqdm(ent[cl_ler].iterrows()):
            pr = dict(rw)
            pr.pop("ID")
            pr = {k.split(":")[1]:v for k,v in pr.items()}
            for k,v in pr.items():
                if not isNaN(v):
                    if not isinstance(v,list):
                        v = [v]
                    ed = [(u,rw["ID"]) for u in v]
                    G.add_edges_from(ed,label=k)   
    return G

def rel2graph(path_rel):
    ENT_R_ENT = os.path.basename(path_rel).split(".")[0]
    ENT1,REL,ENT2 = ENT_R_ENT.split("-")
    # ~ ENT = ENT.split(":")[0]
    print(ENT1,REL,ENT2)
    ent = pd.read_csv(path_rel)
    
    G = nx.DiGraph()
    for ind,rw in tqdm(ent.iterrows()):
        pr = dict(rw)
        ed = (pr["sourceID"],pr["targetID"])
        pr.pop("sourceID")
        pr.pop("targetID")
        pr["label"]=REL
        # ~ print(ed,pr)
        # ~ G.add_edge(*ed,**pr)
        G.add_edge(*ed,label=REL)
        G.nodes[ed[0]]["labels"]=ENT1
        G.nodes[ed[1]]["labels"]=ENT2
          
    return G









PATH = "../data/PROCESSED"



PATH_NODES = join(PATH,"nodes")
PATH_EDGES = join(PATH,"edges")
fls_nodes = glob.glob(join(PATH_NODES,"*.csv"))
fls_edges = glob.glob(join(PATH_EDGES,"*.csv"))

G = nx.DiGraph()
for fn in fls_nodes:

    H = table2graph(fn)
    G = nx.compose(G,H)
    # ~ print(ENT, fn)

for fn in fls_edges:

    R = rel2graph(fn)
    G = nx.compose(G,R)
    # ~ print(fn)



# ATC Ontology
ATC = nx.read_graphml("/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/out/ATC/ATC.graphml")
G = nx.compose(G,ATC)


G = delist_batch(G)


#  ID-ation
ndmp = {nd:nd for nd in G.nodes}
nx.set_node_attributes(G, ndmp, "id")




## TMP: Counts
def to_df(G):
    df = pd.DataFrame.from_dict(dict(G.nodes(data=True)), orient='index')
    return df
print(f" Graph size {len(G)}")
df_n =  to_df(G)
print(df_n.groupby(['labels']).size())



# DUMP #############################
####################################
SAVE = True
if SAVE:
    nx.write_graphml(G, "../out/DRKG_OT.graphml",named_key_ids =True)

