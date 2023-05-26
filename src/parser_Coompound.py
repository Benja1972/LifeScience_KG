

import numpy as np

import networkx as nx
import pandas as pd
from os.path import join

import os
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def isNaN(num):
    return num != num




def cln_list(ll):
    ll = [l for l in ll if not isNaN(l)]
    return ll


PATH ="../data/FDA/Compound/"
ENTITY = "Compound"

# UNII FDA Compounds
frec = join(PATH,"UNII_Records_19Nov2021.txt")
urec = pd.read_csv(frec, index_col=0,sep="\t",dtype= str )

cols = [
        'PUBCHEM',
        'PT',
        "NCIT",
        "RXCUI",
        'INN_ID',
        "INCHIKEY",
        "SMILES"
        ]

urec = urec[cols]



fun =  "../data/FDA/Compound/UNII_Names_19Nov2021.txt"
uni  = pd.read_csv(fun,sep="\t")
uni = uni[["Name","UNII"]]





# ATC
atc = pd.read_csv("/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/out/ATC/ATC_nodes.csv", index_col=0)
atc["lname"] = atc["name"].apply(lambda x: x.lower())
atc["ID"] =  atc.index
matc = atc[["lname","ID"]].groupby("lname").agg({"ID": lambda x: x.unique().tolist()})

matc = dict(matc["ID"])


def map_atc(l):
    mp=[]
    if not isNaN(l):
        l = l.lower()
        if l in matc.keys():
            mp = matc[l]
            if len(mp)>0:
                print(mp)
        
    return mp


uni["ATC"] = uni["Name"].apply(lambda x: map_atc(x))
uni = uni.groupby('UNII').agg({"Name": lambda x: x.unique().tolist(),
                                "ATC": sum})

compd = pd.concat([urec,uni],axis=1)
compd["PUBCHEM"]=compd["PUBCHEM"].apply(lambda x: ["Pubchem.Compound:"+x] if isinstance(x,str) else [])
compd["REL:same_as"] = compd["PUBCHEM"]+compd["ATC"]
compd.drop(["PUBCHEM","ATC"],inplace=True,axis=1)

col_u = {
    "Name":"Synonyms",
    "PT":"Name"
}

compd = compd.rename(columns=col_u)
compd['ID'] = compd.index
compd['ID'] = compd['ID'].apply(lambda x: "UNII:"+str(x))
compd["Synonyms"] = compd["Synonyms"].apply(lambda x: cln_list(x))

def colle(rw):
    loc = ["NCIT",
        "RXCUI",
        'INN_ID',
        "INCHIKEY",
        "SMILES"]
    rw = dict(rw[loc])
    cl = [str(k)+":"+str(v) for k,v in rw.items() if not isNaN(v)]
    return cl

compd["xref"] = compd.apply(lambda r: colle(r), axis=1)

path_out =join(PATH,"Processed")


if not os.path.isdir(path_out):
    try:
        os.mkdir(path_out)
    except OSError:
        print ("Creation of the directory %s failed" % path_out)
    else:
        print ("Successfully created the directory %s" % path_out)


out_col = ['ID',"Name","Synonyms","REL:same_as","xref"]

compd[out_col].to_csv(join(path_out,f"{ENTITY}.csv"),index=False)

