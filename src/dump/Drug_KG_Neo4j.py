
from rdflib import Graph
import numpy as np

import networkx as nx
import pandas as pd
from os.path import join
from tqdm import tqdm
import os

import sys
sys.path.append("/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/src/")

from BioOntoTools import *


def clean(s):
    s = s.replace("(BOVINE;","(BOVINE,")
    s = s.split(";")
    s = [c.strip().replace("(BOVINE,","(BOVINE;") for c in s]

    return s


G = nx.DiGraph()



NSAMPLE = 0


fin = "../data/product.csv"

prod = pd.read_csv(fin, index_col=0, encoding = "ISO-8859-1")
if NSAMPLE >0:
    prod = prod.sample(NSAMPLE)

cols = ['PROPRIETARYNAME',"PRODUCTTYPENAME",'NONPROPRIETARYNAME','LABELERNAME','SUBSTANCENAME']

prod = prod[cols]
prod = prod.drop_duplicates()


fun =  "../data/UNII/UNII_Names_14Sep2021.txt"
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



dl_map_k = dl_map.keys()






###01 Initial drug graph
print("Constructing Drug graph")
for ind,rw in tqdm(prod.iterrows()):
    drug = str(rw["PROPRIETARYNAME"]).lower()
    idrug = "Product_Drug:"+ drug
    drug_type = str(rw["PRODUCTTYPENAME"]).split()
    drug_type = [dr.strip().lower() for dr in drug_type][-1]

    org = str(rw["LABELERNAME"]).strip()
    comp = clean(str(rw["SUBSTANCENAME"]))
    comp = set([dl_map[c] if c in dl_map_k else c for c in comp])
    if "nan" in comp:
        comp.remove("nan")
    
    if org !="nan" and drug !="nan":
        G.add_edge(org,idrug,label="manufactures")
        G.nodes[org]["labels"] = "Company"
        G.nodes[org]["name"] = org
        
        G.nodes[idrug]["labels"] = "Drug_Product"
        G.nodes[idrug]["name"] = drug
        
        if drug_type !="nan":
             G.nodes[idrug]["drug_type"] = drug_type
             # ~ print(drug_type)
    
    if len(comp)>0 and drug !="nan":

        for uc in comp:
            uii_uc = "UNII_"+str(uni.loc[uc]["UNII"])
            # ~ print(uc, uii_uc)
            G.add_edge(idrug,uii_uc,label="has_ingredient")
            G.nodes[uii_uc]["labels"] = "Compound"
            G.nodes[uii_uc]["name"] = uc
            G.nodes[idrug]["labels"] = "Drug_Product"
            G.nodes[idrug]["name"] = drug







## Group drugs
GROUP = False
if GROUP:
    odrl = [nd for nd in G.nodes if G.nodes[nd]["labels"] =="Drug_Product"]
    for u, v in itertools.combinations(odrl, 2):
        us = set([ic for ic in list(G.successors(u)) if G.nodes[ic]["labels"]=="Compound"])
        vs = set([ic for ic in list(G.successors(v)) if G.nodes[ic]["labels"]=="Compound"])
        if len(us) >0 and us == vs:
            print(u, "< - >", v)
            G.add_edge(u,v,label="similarTo")
            G.add_edge(v,u,label="similarTo")




## Interactions

if True:

    # extract for linking
    # ~ odrl = [nd for nd in G.nodes if G.nodes[nd]["labels"] =="Drug_Product"]
    ocm = [(nd,G.nodes[nd]["name"].lower()) for nd in G.nodes if G.nodes[nd]["labels"] =="Compound"]

    
    
    ##02 Drug -> Gene interaction
    dg = "../data/drug_gene_interactions.csv"
    dr_gn = pd.read_csv(dg)
    if NSAMPLE >0:
        dr_gn = dr_gn.sample(NSAMPLE)
    
    cls = ["gene_name","drug_claim_name","drug_claim_primary_name","drug_name","drug_concept_id"]
    dr_gn = dr_gn[cls]
    
    
    
    print("Drug -> Gene interaction")
    for ind,rw in tqdm(dr_gn.iterrows()):
        gn = str(rw["gene_name"])
        drs = list(rw[["drug_claim_name","drug_claim_primary_name","drug_name"]])
        drs = [str(dr) for dr in drs]
        drs = list(set([dr.lower() for dr in drs if dr !="nan"]))
        
        if gn !="nan" and len(drs)>0:
            for oc in ocm:
                if oc[1] in drs:
                    G.add_edge(oc[0],gn,label="targets")
                    G.nodes[gn]["labels"] = "_Gene"
                    G.nodes[gn]["name"] = gn

    
    ##03 Drug -> Protein interaction
    dp = "../data/drug_target_interaction.csv"
    dr_pt = pd.read_csv(dp)
    if NSAMPLE >0:
        dr_pt = dr_pt.sample(NSAMPLE)
    
    cpls = ["DRUG_NAME","ACCESSION"]
    dr_pt = dr_pt[cpls]
    
    
    
    print("Drug -> Protein interaction")
    for ind,rw in tqdm(dr_pt.iterrows()):
        drr = str(rw["DRUG_NAME"]).lower()
        pts = str(rw["ACCESSION"])
        pts = pts.split("|")
        pts = [pt for pt in pts if pt !="nan"]
        
        if drr !="nan" and len(pts)>0:
            for oc in ocm:
                if oc[1] ==drr:
                    for pt in pts:
                        G.add_edge(oc[0],pt,label="acts_on")
                        G.nodes[pt]["labels"] = "_Protein"
                        G.nodes[pt]["name"] = pt





ATC = True
    
if ATC:
    ##04 ATC Ontology annotation
    fg = "/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/out/ATC/ATC.graphml"
    AT  = nx.read_graphml(fg)
    
    # Re-name
    for nd in AT.nodes:
        att = AT.nodes[nd]
        att["name"] = att.pop("label")
    for ed in AT.edges:
        att = AT.edges[ed]
        att["label"] = att.pop("type")
    
    # Update

    nx.set_node_attributes(AT, "Medical_concept", "labels")
    
    
    # ~ drg_nd = [nd for nd in G.nodes if G.nodes[nd]["labels"] in ["Compound","Drug"]]
    drg_nd = [(nd,G.nodes[nd]["name"].lower()) for nd in G.nodes if G.nodes[nd]["labels"] in ["Compound"]]
    
    
    GAT = nx.compose(G,AT)
    print("ATC Ontology annotation")
    for d in tqdm(drg_nd):
        for at in AT.nodes:
            if d[1].lower()== AT.nodes[at]["name"].lower():
                GAT.add_edge(d[0],at,label="onto_xref")
            # ~ elif "generic" in G.nodes[d] and  G.nodes[d]["generic"].lower()== AT.nodes[at]["name"].lower():
                # ~ GAT.add_edge(d[0],at,label="onto_xref")
    G = GAT

            
    

#  ID-ation
ndmp = {nd:nd for nd in G.nodes}
nx.set_node_attributes(G, ndmp, "id")




## TMP: Counts
print(f" Graph size {len(G)}")
df_n, df_e =  to_DF(G)
print(df_n.groupby(['labels']).size())



# DUMP #############################
####################################
SAVE = True
if SAVE:
    nx.write_graphml(G, "../out/DRKG.graphml",named_key_ids =True)


