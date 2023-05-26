from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

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

PATH ="../data/OpenTargets"
ENTITY_FLD = "evidence/sourceId=chembl"



path_out = "../data/PROCESSED/edges"

frec = join(PATH,ENTITY_FLD)


spark = (SparkSession.builder.master('local[*]').getOrCreate())

dis = spark.read.parquet(frec)
dis.printSchema()
disS = (dis
     .select("drugId",
            "diseaseId",
             "studyId",
             "urls",
             "clinicalPhase"))

df = disS.toPandas()

def map_ct(rw):
    # ~ rw = rw["urls"]
    rw = [r.asDict() for r in rw]
    rw = [r["niceName"]+":"+r["url"].split("id=")[-1].replace("%22","") for r in rw]
    rw = [r for r in rw if r.startswith("ClinicalT")]
    if len(rw)==1:
        rw = rw[0]
    else:
        rw = None
    return rw




df["CT"] = df["urls"].apply(lambda x: map_ct(x))
df = df.dropna(subset=["CT"])

## Disease to CT
ds_c = df[["CT","diseaseId","clinicalPhase"]]

col_u = {
    "CT":"sourceID",
    "diseaseId":"targetID",
}

ds_c = ds_c.rename(columns=col_u)

ENTITY1 = "Clinical_study"
ENTITY2 = "Disease"
REL ="studies"
foutCD =f"{ENTITY1}-{REL}-{ENTITY2}.csv"
ds_c.to_csv(join(path_out,foutCD),index=False)

##  CT to Compound
c_c = df[["drugId","CT","clinicalPhase"]]

col_u = {
    "drugId":"sourceID",
    "CT":"targetID",
}

c_c = c_c.rename(columns=col_u)

ENTITY1 = "Compound"
ENTITY2 = "Clinical_study"
REL ="is_validated_in"
foutCC =f"{ENTITY1}-{REL}-{ENTITY2}.csv"
c_c.to_csv(join(path_out,foutCC),index=False)




# Convert to a Pandas Dataframe
# ~ df = dis.toPandas()


# ~ col_u = {
    # ~ "diseaseId":"sourceID",
    # ~ "targetId":"targetID",
# ~ }

# ~ df = df.rename(columns=col_u)

# ~ df.to_csv(join(path_out,fout),index=False)






if False:


    def map_pubch(l):
        mp=[]
        if isinstance(l,dict) and "PubChem" in l.keys():
            mp = ["Pubchem.Compound:"+x for x in l["PubChem"]]
            
        return mp

    def map_linked(l):
        mp=[]
        if l is not None :
            mp = list(l[0])

        return mp


    df["REL:same_as"] = df["xref"].apply(lambda x: map_pubch(x))

    df["REL:targets"] = df["linkedTargets"].apply(lambda x: map_linked(x))
    df["REL:has_effect_on"] = df["linkedDiseases"].apply(lambda x: map_linked(x))
    df.drop(["linkedTargets","linkedDiseases"],inplace=True,axis=1)


    df.to_csv(join(path_out,f"{ENTITY}.csv"),index=False)

# ~ urec = pd.read_csv(frec, index_col=0,sep="\t",dtype= str )

# ~ cols = [
        # ~ 'PUBCHEM',
        # ~ 'PT',
        # ~ "NCIT",
        # ~ "RXCUI",
        # ~ 'INN_ID',
        # ~ "INCHIKEY",
        # ~ "SMILES"
        # ~ ]

# ~ urec = urec[cols]



# ~ fun =  "../data/FDA/Compound/UNII_Names_19Nov2021.txt"
# ~ uni  = pd.read_csv(fun,sep="\t")
# ~ uni = uni[["Name","UNII"]]





# ~ # ATC
# ~ atc = pd.read_csv("/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/out/ATC/ATC_nodes.csv", index_col=0)
# ~ atc["lname"] = atc["name"].apply(lambda x: x.lower())
# ~ atc["ID"] =  atc.index
# ~ matc = atc[["lname","ID"]].groupby("lname").agg({"ID": lambda x: x.unique().tolist()})

# ~ matc = dict(matc["ID"])


# ~ def map_atc(l):
    # ~ mp=[]
    # ~ if not isNaN(l):
        # ~ l = l.lower()
        # ~ if l in matc.keys():
            # ~ mp = matc[l]
            # ~ if len(mp)>0:
                # ~ print(mp)
        
    # ~ return mp


# ~ uni["ATC"] = uni["Name"].apply(lambda x: map_atc(x))
# ~ uni = uni.groupby('UNII').agg({"Name": lambda x: x.unique().tolist(),
                                # ~ "ATC": sum})

# ~ compd = pd.concat([urec,uni],axis=1)
# ~ compd["PUBCHEM"]=compd["PUBCHEM"].apply(lambda x: ["Pubchem.Compound:"+x] if isinstance(x,str) else [])
# ~ compd["REL:same_as"] = compd["PUBCHEM"]+compd["ATC"]
# ~ compd.drop(["PUBCHEM","ATC"],inplace=True,axis=1)

# ~ col_u = {
    # ~ "Name":"Synonyms",
    # ~ "PT":"Name"
# ~ }

# ~ compd = compd.rename(columns=col_u)
# ~ compd['ID'] = compd.index
# ~ compd['ID'] = compd['ID'].apply(lambda x: "UNII:"+str(x))
# ~ compd["Synonyms"] = compd["Synonyms"].apply(lambda x: cln_list(x))

# ~ def colle(rw):
    # ~ loc = ["NCIT",
        # ~ "RXCUI",
        # ~ 'INN_ID',
        # ~ "INCHIKEY",
        # ~ "SMILES"]
    # ~ rw = dict(rw[loc])
    # ~ cl = [str(k)+":"+str(v) for k,v in rw.items() if not isNaN(v)]
    # ~ return cl

# ~ compd["xref"] = compd.apply(lambda r: colle(r), axis=1)

# ~ path_out =join(PATH,"Processed")


# ~ if not os.path.isdir(path_out):
    # ~ try:
        # ~ os.mkdir(path_out)
    # ~ except OSError:
        # ~ print ("Creation of the directory %s failed" % path_out)
    # ~ else:
        # ~ print ("Successfully created the directory %s" % path_out)


# ~ out_col = ['ID',"Name","Synonyms","REL:same_as","xref"]

# ~ compd[out_col].to_csv(join(path_out,f"{ENTITY}.csv"),index=False)

