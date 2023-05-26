
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

G = nx.DiGraph()
# ~ G = nx.MultiDiGraph()


def clean(s):
    s = s.replace("(BOVINE;","(BOVINE,")
    s = s.split(";")
    s = [c.strip().replace("(BOVINE,","(BOVINE;") for c in s]

    return s


fin = "../data/product.csv"
# ~ fdb =  "../data/DrugBank/drugbank_vocabulary.csv"
fun =  "../data/UNII/UNII_Names_14Sep2021.txt"

prod = pd.read_csv(fin, index_col=0, encoding = "ISO-8859-1")
uni  = pd.read_csv(fun, index_col=0,sep="\t")
uni = uni.dropna()

IND = list(set(uni.index))

cols = ['PROPRIETARYNAME',"PRODUCTTYPENAME",'NONPROPRIETARYNAME','LABELERNAME','SUBSTANCENAME']
# ~ col_db = ["Common name","UNII","Synonyms"]


prod = prod[cols]
prod = prod.drop_duplicates()


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

compAll = []


dl_map_k = dl_map.keys()

cnt = 0

###01 Initial drug graph
print("Constructing Drug graph")
for ind,rw in tqdm(prod.iterrows()):

    comp = clean(str(rw["SUBSTANCENAME"]))
    comp = set([dl_map[c] if c in dl_map_k else c for c in comp])
    if "nan" in comp:
        comp.remove("nan")
    
    
    # ~ if "nan" not in comp:
    compAll+=list(comp)
        

    


        
compAll =  set(compAll)

dl = compAll -set(IND)




# ~ db_nm = list(db["Common name"])
# ~ db_nm = [db.lower() for db in db_nm]

# ~ db_nm = set(db_nm)

# ~ no_cmp = compAll - db_nm


# ~ print(f"Compounds {len(compAll)}, common in DB {len(compAll&db_nm)}")

    
    # ~ if org !="nan" and drug !="nan":
        # ~ G.add_edge(org,idrug,type="manufactures")
        # ~ G.nodes[org]["type"] = "company"
        # ~ G.nodes[org]["label"] = org
        
        # ~ G.nodes[idrug]["type"] = "drug"
        # ~ G.nodes[idrug]["label"] = drug
        
        # ~ if ndrug !="nan":
             # ~ G.nodes[idrug]["generic"] = ndrug
        # ~ if drug_type !="nan":
             # ~ G.nodes[idrug]["drug_type"] = drug_type
             # ~ print(drug_type)
    
    # ~ if comp !="nan" and drug !="nan":
        # ~ comp = comp.split(";")
        # ~ comp = [c.strip().lower() for c in comp]
    
        # ~ for uc in comp:
            # ~ G.add_edge(idrug,uc,type="has_ingredient")
            # ~ G.nodes[uc]["type"] = "compound"
            # ~ G.nodes[uc]["label"] = uc
            # ~ G.nodes[idrug]["type"] = "drug"
            # ~ G.nodes[idrug]["label"] = drug
            # ~ if ndrug !="nan":
                 # ~ G.nodes[idrug]["generic"] = ndrug





if False:
    ## Group drugs
    odrl = [nd for nd in G.nodes if G.nodes[nd]["type"] =="drug"]
    for u, v in itertools.combinations(odrl, 2):
        us = set([ic for ic in list(G.successors(u)) if G.nodes[ic]["type"]=="compound"])
        vs = set([ic for ic in list(G.successors(v)) if G.nodes[ic]["type"]=="compound"])
        if len(us) >0 and us == vs:
            print(u, "< - >", v)
            G.add_edge(u,v,type="sameAs")
            G.add_edge(v,u,type="sameAs")
    
    
    nx.write_graphml(G, "../out/_test_DRKG.graphml")
    
    ## Interactions
    
    if False:
    
        # extract for linking
        odrl = [nd for nd in G.nodes if G.nodes[nd]["type"] =="drug"]
        ocm = [nd for nd in G.nodes if G.nodes[nd]["type"] =="compound"]
        
        # ~ odrl = []
        # ~ for oc in odr:
            # ~ lb = G.nodes[oc]["label"]
            # ~ ics = [ic for ic in list(G.successors(oc)) if G.nodes[ic]["type"]=="compound"]
            # ~ gnrc = G.nodes[oc]["generic"].lower() if "generic" in G.nodes[oc] else ""
            # ~ als = [lb]+[gnrc]
            # ~ cnta = set(als)&set(ics)
            # ~ if len(cnta)==0:
                # ~ odrl.append(oc)
                
            
        
        
        
        ##02 Drug -> Gene interaction
        dg = "../data/drug_gene_interactions.csv"
        dr_gn = pd.read_csv(dg)
        dr_gn = dr_gn.sample(500)
        
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
                    if oc in drs:
                        G.add_edge(oc,gn,type="targets")
                        G.nodes[gn]["type"] = "gene"
                        G.nodes[gn]["label"] = gn
                        # ~ print(oc," -> ", gn)
                for od in odrl:
                    gnrc = G.nodes[od]["generic"].lower() if "generic" in G.nodes[od] else ""
                    od_l = [G.nodes[od]["label"]]+[gnrc]
                    ise = set(od_l)&set(drs)
                    if len(ise)>0:
                        G.add_edge(od,gn,type="targets")
                        G.nodes[gn]["type"] = "gene"
                        G.nodes[gn]["label"] = gn
                        # ~ print(od," -> ", gn)
                
            
        
        
        
        
        ##03 Drug -> Protein interaction
        dp = "../data/drug_target_interaction.csv"
        dr_pt = pd.read_csv(dp)
        dr_pt = dr_pt.sample(500)
        
        cpls = ["DRUG_NAME","ACCESSION"]
        dr_pt = dr_pt[cpls]
        
        
        
        print("Drug -> Protein interaction")
        for ind,rw in tqdm(dr_pt.iterrows()):
            drr = str(rw["DRUG_NAME"]).lower()
            pts = str(rw["ACCESSION"])
            pts = pts.split("|")
            pts = [pt for pt in pts if pt !="nan"]
            
            if drr !="nan" and len(pts)>0:
                if drr in ocm:
                    for pt in pts:
                        G.add_edge(drr,pt,type="acts_on")
                        G.nodes[pt]["type"] = "protein"
                        G.nodes[pt]["label"] = pt
                        # ~ print(drr," -> ", pt)
                for od in odrl:
                    gnrc = G.nodes[od]["generic"].lower() if "generic" in G.nodes[od] else ""
                    od_l = [G.nodes[od]["label"]]+[gnrc]
                    if drr in set(od_l):
        
                        for pt in pts:
                            G.add_edge(od,pt,type="acts_on")
                            G.nodes[pt]["type"] = "protein"
                            G.nodes[pt]["label"] = pt
                            # ~ print(od," -> ", pt)
        
        
        
    
    
    
    
    
    
    
    
    # ~ if False:
        ##04 ATC Ontology annotation
        fg = "/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/out/ATC/ATC.graphml"
        AT  = nx.read_graphml(fg,force_multigraph=True)
        nx.set_node_attributes(AT, "medical_concept", "type")
        
        
        drg_nd = [nd for nd in G.nodes if G.nodes[nd]["type"] in ["compound","drug"]]
        
        
        GAT = nx.compose(G,AT)
        print("ATC Ontology annotation")
        for d in tqdm(drg_nd):
            for at in AT.nodes:
                if d.lower()== AT.nodes[at]["label"].lower():
                    GAT.add_edge(d,at,type="onto_xref")
                elif "generic" in G.nodes[d] and  G.nodes[d]["generic"].lower()== AT.nodes[at]["label"].lower():
                    GAT.add_edge(d,at,type="onto_xref")
        G = GAT
    
                
        
    
    
    
    
    
    # DUMP
    SAVE = False
    if SAVE:
        nx.write_graphml(G, "../out/DRKG.graphml")
    
        df_n, df_e =  to_DF(G)
    
        df_n.to_csv("../out/DRKG_nodes.csv")
        df_e.to_csv("../out/DRKG_edges.csv")
    
    
    
    ## TMP: Counts
    print(f" Graph size {len(G)}")
    df_n, df_e =  to_DF(G)
    print(df_n.groupby(['type']).size())
    
    ############
    
    
    
