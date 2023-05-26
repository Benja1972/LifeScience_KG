
# ~ from rdflib import Graph
import numpy as np

# ~ import networkx as nx
import pandas as pd
from os.path import join
from tqdm import tqdm
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# ~ import sys
# ~ sys.path.append("/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/src/")

# ~ from BioOntoTools import *

def isNaN(num):
    return num != num



def lst_lst(ll,sep=","):
    ll = [l for l in ll if not isNaN(l)]
    if sep==";":
        ll = [l.replace("(BOVINE;","(BOVINE,").replace("(ENZYMATIC;","(ENZYMATIC,") for l in ll]
        # ~ ll = [l.replace("(ENZYMATIC;","(ENZYMATIC,") for l in ll]
    if len(ll)>0:
        lo = [l.split(sep) for l in ll]
        lo = list(set([l.strip().replace("(BOVINE,","(BOVINE;").replace("(ENZYMATIC,","(ENZYMATIC;") for ol in lo for l in ol]))
    else:
        lo = []
    return list(set(lo))

def lst_un(ll):
    ll = [l for l in ll if not isNaN(l)]
    if len(ll)>0:
        lo = list(set(ll))
    else:
        lo = []
    return lo





NSAMPLE = 0

PATH ="../data/FDA/Drug_product/"
ENTITY = "Drug"


fin = join(PATH,"product.txt")

prodo = pd.read_csv(fin, index_col=0, encoding = "ISO-8859-1",sep="\t")
if NSAMPLE >0:
    prodo = prodo.sample(NSAMPLE)


cols = ['PRODUCTNDC',
        "MARKETINGCATEGORYNAME",
        "APPLICATIONNUMBER",
        'PROPRIETARYNAME',
        'NONPROPRIETARYNAME',
        "PRODUCTTYPENAME",
        "PHARM_CLASSES",
        'LABELERNAME',
        'SUBSTANCENAME']

prod = prodo[cols]
prod = prod.drop_duplicates()
prod['NONPROPRIETARY_NAME'] = prod['NONPROPRIETARYNAME'].apply(lambda x: x.upper() if not isNaN(x) else '')
prod['PROPRIETARY_NAME'] = prod['PROPRIETARYNAME'].apply(lambda x: x.upper() if not isNaN(x) else '')




if False:



    prod = prod.groupby('PRODUCTNDC').agg({"PRODUCTTYPENAME": lambda x: x.unique().tolist(), #'first', 
                                          "APPLICATIONNUMBER": lambda x: x.unique().tolist(),
                                          "MARKETINGCATEGORYNAME": lambda x: x.unique().tolist(),
                                          "PROPRIETARYNAME": lambda x: x.unique().tolist(),
                                          "NONPROPRIETARYNAME": lambda x: x.unique().tolist(),
                                          "PHARM_CLASSES": lambda x: x.unique().tolist(),
                                          "LABELERNAME": lambda x: x.unique().tolist(),
                                          "SUBSTANCENAME": lambda x: x.unique().tolist()
                                          })




    prod['PRODUCTTYPENAME'] = prod['PRODUCTTYPENAME'].apply(lambda x: lst_un(x))
    prod['APPLICATIONNUMBER'] = prod['APPLICATIONNUMBER'].apply(lambda x: lst_un(x))
    prod["MARKETINGCATEGORYNAME"] = prod["MARKETINGCATEGORYNAME"].apply(lambda x: lst_un(x))
    prod['PROPRIETARYNAME'] = prod['PROPRIETARYNAME'].apply(lambda x: lst_un(x))
    prod['NONPROPRIETARYNAME'] = prod['NONPROPRIETARYNAME'].apply(lambda x: lst_un(x))
    prod['PHARM_CLASSES'] = prod['PHARM_CLASSES'].apply(lambda x: lst_lst(x,sep=","))
    prod['LABELERNAME'] = prod['LABELERNAME'].apply(lambda x: lst_un(x))
    prod['SUBSTANCENAME'] = prod['SUBSTANCENAME'].apply(lambda x: lst_lst(x,sep=";"))


    prod.index.rename(name = "NDC:ID", inplace=True)
    prod['ID'] = prod.index
    prod['ID'] = prod['ID'].apply(lambda x: "NDC:"+str(x))



    col_map = {
        'PRODUCTTYPENAME':'Product_type',
        "MARKETINGCATEGORYNAME":"Marketing_category",
        'APPLICATIONNUMBER':'Application_number',
        'PROPRIETARYNAME':'Proprietary_name',
        "NONPROPRIETARYNAME": "Generic_name",
        "PHARM_CLASSES":"Pharm_classes",
        "LABELERNAME":"Company",
        "SUBSTANCENAME":"Compounds"
    }
    prod = prod.rename(columns=col_map)


    path_out =join(PATH,"Processed")


    if not os.path.isdir(path_out):
        try:
            os.mkdir(path_out)
        except OSError:
            print ("Creation of the directory %s failed" % path_out)
        else:
            print ("Successfully created the directory %s" % path_out)




    # Map Compounds to UNII

    fun =  "../data/FDA/Compound/UNII_Names_19Nov2021.txt"
    uni  = pd.read_csv(fun, index_col=0,sep="\t")
    uni = uni.dropna()

    IND = list(set(uni.index))




    dl_map ={
             'MAMMAL LIVER':"nan",
             'VIABLE AND METABOLICALLY ACTIVE ALLOGENEIC HUMAN NIKS KERATINOCYTES AND HUMAN DERMAL FIBROBLASTS CELLULARIZED LAYERED SCAFFOLD':"nan",
             "BALLOTA FOETIDA":"BALLOTA NIGRA WHOLE",
             '.BETA.-CAROTENE':'.BETA.-CAROTENE [MI]',
             'AMANITA MUSCARIA VAR. MUSCARIA':"AMANITA MUSCARIA VAR. MUSCARIA [WHO-DD]",
             'CHIONANTHUS VIRGINICUS BARK':"CHIONANTHUS VIRGINICUS ROOT BARK",
             'COLLINSONIA': "COLLINSONIA [MI]",
             'CONYZA CANADENSIS': "CONYZA CANADENSIS [WHO-DD]",
             'ERYSIMUM CHEIRI':'ERYSIMUM CHEIRI WHOLE',
             'GENISTA TINCTORIA':"GENISTA TINCTORIA [HPUS]",
             'HYALURONIDASE': "HYALURONIDASE [WHO-DD]",
             'INTERLEUKIN-3':"INTERLEUKIN-3 RECEPTOR SUBUNIT ALPHA",
             'PARIETARIA OFFICINALIS':'PARIETARIA OFFICINALIS [WHO-DD]',
             'PAROXETINE HYDROCHLORIDE HEMIHYDRATE':"PAROXETINE HYDROCHLORIDE HEMIHYDRATE [WHO-DD]",
             'PLANTAGO LANCEOLATA':"PLANTAGO LANCEOLATA [WHO-DD]",
             'PRUNUS SPINOSA BUDDING TOP':"PRUNUS SPINOSA FLOWER BUD"}





    def map_unii(ls):
        ls = set([dl_map[c] if c in dl_map.keys() else c for c in ls])
        if "nan" in ls:
            ls.remove("nan")
        uii_uc = ["UNII:"+str(uni.loc[uc]["UNII"]) for uc in ls]
        return uii_uc
        


    prod["REL:has_ingredient"] = prod["Compounds"].apply(map_unii)



    # Save
    clmns = ['ID'] + list([a for a in prod.columns if a != 'ID'])
    prod[clmns].to_csv(join(path_out,f"{ENTITY}.csv"),index=False)


