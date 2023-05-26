
from rdflib import Graph
import numpy as np

import networkx as nx
import pandas as pd
from os.path import join
from tqdm import tqdm
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def isNaN(num):
    return num != num




def lst_lst(ll,sep=","):
    # ~ ll = [l for l in ll if not isNaN(l)]
    if not isNaN(ll):
        lo = ll.split(sep)
        lo = [l.strip() for l in lo]
    else:
        lo = []
    return lo


PATH ="../data/FDA/Company/"
ENTITY = "Company"


fin = join(PATH,"drls_reg.txt")

prodo = pd.read_csv(fin, index_col=0, encoding = "ISO-8859-1",sep="\t")



## HQ companies
cols = ["REGISTRANT_DUNS",
        "REGISTRANT_NAME",
        "REGISTRANT_CONTACT_NAME",
        "REGISTRANT_CONTACT_EMAIL"]



prod = prodo[cols]
prod = prod.drop_duplicates()

prod['REGISTRANT_DUNS'] = prod['REGISTRANT_DUNS'].apply(lambda x: "DUNS:"+str(x))
prod['REGISTRANT_NAME'] = prod['REGISTRANT_NAME'].apply(lambda x: str(x).strip())
prod['REGISTRANT_CONTACT_NAME'] = prod['REGISTRANT_CONTACT_NAME'].apply(lambda x: str(x).strip())
prod['REGISTRANT_CONTACT_EMAIL'] = prod['REGISTRANT_CONTACT_EMAIL'].apply(lambda x: str(x).strip())

col_map = {
    'REGISTRANT_NAME':'Name',
    "REGISTRANT_DUNS":"ID",
    'REGISTRANT_CONTACT_NAME':'Contact_name',
    'REGISTRANT_CONTACT_EMAIL':'Contact_email',
}

prod = prod.rename(columns=col_map)



## SB companies
colss = [
        "DUNS_NUMBER",
        "FIRM_NAME",
        "ADDRESS",
        "OPERATIONS",
        "ESTABLISHMENT_CONTACT_NAME",
        "ESTABLISHMENT_CONTACT_EMAIL",
        "REGISTRANT_DUNS"
        ]

comp = prodo[colss]
comp = comp.drop_duplicates()

comp['DUNS_NUMBER'] = comp['DUNS_NUMBER'].apply(lambda x: "DUNS:"+str(x))
comp['REGISTRANT_DUNS'] = comp['REGISTRANT_DUNS'].apply(lambda x: "DUNS:"+str(x))
comp['OPERATIONS'] = comp['OPERATIONS'].apply(lambda x: lst_lst(x,sep=";"))

comp['FIRM_NAME'] = comp['FIRM_NAME'].apply(lambda x: str(x).strip())
comp["ADDRESS"] = comp["ADDRESS"].apply(lambda x: str(x).strip())
comp["ESTABLISHMENT_CONTACT_NAME"] = comp["ESTABLISHMENT_CONTACT_NAME"].apply(lambda x: str(x).strip())
comp["ESTABLISHMENT_CONTACT_EMAIL"] = comp["ESTABLISHMENT_CONTACT_EMAIL"].apply(lambda x: str(x).strip())




coll_map = {
    'FIRM_NAME':'Name',
    "DUNS_NUMBER":"ID",
    "OPERATIONS":"Business_operations",
    "ADDRESS":"Address",
    'ESTABLISHMENT_CONTACT_NAME':'Contact_name',
    'ESTABLISHMENT_CONTACT_EMAIL':'Contact_email',
    'REGISTRANT_DUNS':"REL:is_subsidiary_of"
}

comp = comp.rename(columns=coll_map)
comp.index.rename(name = "FEI:ID", inplace=True)





compn = pd.concat([prod, comp], axis=0, ignore_index=True) 

compn = compn.groupby('ID').first()


compn['ID'] = compn.index








## Save


path_out =join(PATH,"Processed")


if not os.path.isdir(path_out):
    try:
        os.mkdir(path_out)
    except OSError:
        print ("Creation of the directory %s failed" % path_out)
    else:
        print ("Successfully created the directory %s" % path_out)


compn.to_csv(join(path_out,f"{ENTITY}.csv"),index=False)



# ~ prod['PRODUCTTYPENAME'] = prod['PRODUCTTYPENAME'].apply(lambda x: lst_un(x))
# ~ prod['APPLICATIONNUMBER'] = prod['APPLICATIONNUMBER'].apply(lambda x: lst_un(x))
# ~ prod["MARKETINGCATEGORYNAME"] = prod["MARKETINGCATEGORYNAME"].apply(lambda x: lst_un(x))
# ~ prod['PROPRIETARYNAME'] = prod['PROPRIETARYNAME'].apply(lambda x: lst_un(x))
# ~ prod['NONPROPRIETARYNAME'] = prod['NONPROPRIETARYNAME'].apply(lambda x: lst_un(x))
# ~ prod['PHARM_CLASSES'] = prod['PHARM_CLASSES'].apply(lambda x: lst_lst(x,sep=","))
# ~ prod['LABELERNAME'] = prod['LABELERNAME'].apply(lambda x: lst_un(x))
# ~ prod['SUBSTANCENAME'] = prod['SUBSTANCENAME'].apply(lambda x: lst_lst(x,sep=";"))




















# ~ path_out =join(PATH,"Processed")


# ~ if not os.path.isdir(path_out):
    # ~ try:
        # ~ os.mkdir(path_out)
    # ~ except OSError:
        # ~ print ("Creation of the directory %s failed" % path_out)
    # ~ else:
        # ~ print ("Successfully created the directory %s" % path_out)




# ~ # Map Compounds to UNII

# ~ fun =  "../data/FDA/UNII/UNII_Names_19Nov2021.txt"
# ~ uni  = pd.read_csv(fun, index_col=0,sep="\t")
# ~ uni = uni.dropna()

# ~ IND = list(set(uni.index))




# ~ dl_map ={
         # ~ 'MAMMAL LIVER':"nan",
         # ~ 'VIABLE AND METABOLICALLY ACTIVE ALLOGENEIC HUMAN NIKS KERATINOCYTES AND HUMAN DERMAL FIBROBLASTS CELLULARIZED LAYERED SCAFFOLD':"nan",
         # ~ "BALLOTA FOETIDA":"BALLOTA NIGRA WHOLE",
         # ~ '.BETA.-CAROTENE':'.BETA.-CAROTENE [MI]',
         # ~ 'AMANITA MUSCARIA VAR. MUSCARIA':"AMANITA MUSCARIA VAR. MUSCARIA [WHO-DD]",
         # ~ 'CHIONANTHUS VIRGINICUS BARK':"CHIONANTHUS VIRGINICUS ROOT BARK",
         # ~ 'COLLINSONIA': "COLLINSONIA [MI]",
         # ~ 'CONYZA CANADENSIS': "CONYZA CANADENSIS [WHO-DD]",
         # ~ 'ERYSIMUM CHEIRI':'ERYSIMUM CHEIRI WHOLE',
         # ~ 'GENISTA TINCTORIA':"GENISTA TINCTORIA [HPUS]",
         # ~ 'HYALURONIDASE': "HYALURONIDASE [WHO-DD]",
         # ~ 'INTERLEUKIN-3':"INTERLEUKIN-3 RECEPTOR SUBUNIT ALPHA",
         # ~ 'PARIETARIA OFFICINALIS':'PARIETARIA OFFICINALIS [WHO-DD]',
         # ~ 'PAROXETINE HYDROCHLORIDE HEMIHYDRATE':"PAROXETINE HYDROCHLORIDE HEMIHYDRATE [WHO-DD]",
         # ~ 'PLANTAGO LANCEOLATA':"PLANTAGO LANCEOLATA [WHO-DD]",
         # ~ 'PRUNUS SPINOSA BUDDING TOP':"PRUNUS SPINOSA FLOWER BUD"}





# ~ def map_unii(ls):
    # ~ ls = set([dl_map[c] if c in dl_map.keys() else c for c in ls])
    # ~ if "nan" in ls:
        # ~ ls.remove("nan")
    # ~ uii_uc = [str(uni.loc[uc]["UNII"]) for uc in ls]
    # ~ return uii_uc
    


# ~ prod["UNII:ID"] = prod["Compounds"].apply(map_unii)



# ~ # Save
# ~ prod.to_csv(join(path_out,f"{ENTITY}.csv"))


###01 Initial drug graph
# ~ print("Constructing Drug graph")
# ~ for ind,rw in tqdm(prod.iterrows()):
    # ~ drug = str(rw["PROPRIETARYNAME"]).lower()
    # ~ idrug = "Product_Drug:"+ drug
    # ~ drug_type = str(rw["PRODUCTTYPENAME"]).split()
    # ~ drug_type = [dr.strip().lower() for dr in drug_type][-1]

    # ~ org = str(rw["LABELERNAME"]).strip()
    # ~ comp = clean(str(rw["SUBSTANCENAME"]))
    # ~ comp = set([dl_map[c] if c in dl_map_k else c for c in comp])
    # ~ if "nan" in comp:
        # ~ comp.remove("nan")
    
    # ~ if org !="nan" and drug !="nan":
        # ~ G.add_edge(org,idrug,label="manufactures")
        # ~ G.nodes[org]["labels"] = "Company"
        # ~ G.nodes[org]["name"] = org
        
        # ~ G.nodes[idrug]["labels"] = "Drug_Product"
        # ~ G.nodes[idrug]["name"] = drug
        
        # ~ if drug_type !="nan":
             # ~ G.nodes[idrug]["drug_type"] = drug_type
             # ~ print(drug_type)
    
    # ~ if len(comp)>0 and drug !="nan":

        # ~ for uc in comp:
            # ~ uii_uc = "UNII_"+str(uni.loc[uc]["UNII"])
            # ~ print(uc, uii_uc)
            # ~ G.add_edge(idrug,uii_uc,label="has_ingredient")
            # ~ G.nodes[uii_uc]["labels"] = "Compound"
            # ~ G.nodes[uii_uc]["name"] = uc
            # ~ G.nodes[idrug]["labels"] = "Drug_Product"
            # ~ G.nodes[idrug]["name"] = drug






#  ID-ation
# ~ ndmp = {nd:nd for nd in G.nodes}
# ~ nx.set_node_attributes(G, ndmp, "id")




## TMP: Counts
# ~ print(f" Graph size {len(G)}")
# ~ df_n, df_e =  to_DF(G)
# ~ print(df_n.groupby(['labels']).size())



# DUMP #############################
####################################
# ~ SAVE = False
# ~ if SAVE:
    # ~ nx.write_graphml(G, "../out/DRKG.graphml",named_key_ids =True)








## Group drugs
# ~ GROUP = False
# ~ if GROUP:
    # ~ odrl = [nd for nd in G.nodes if G.nodes[nd]["labels"] =="Drug_Product"]
    # ~ for u, v in itertools.combinations(odrl, 2):
        # ~ us = set([ic for ic in list(G.successors(u)) if G.nodes[ic]["labels"]=="Compound"])
        # ~ vs = set([ic for ic in list(G.successors(v)) if G.nodes[ic]["labels"]=="Compound"])
        # ~ if len(us) >0 and us == vs:
            # ~ print(u, "< - >", v)
            # ~ G.add_edge(u,v,label="similarTo")
            # ~ G.add_edge(v,u,label="similarTo")




# ~ ## Interactions

# ~ if True:

    # ~ # extract for linking
    # ~ odrl = [nd for nd in G.nodes if G.nodes[nd]["labels"] =="Drug_Product"]
    # ~ ocm = [(nd,G.nodes[nd]["name"].lower()) for nd in G.nodes if G.nodes[nd]["labels"] =="Compound"]

    
    
    # ~ ##02 Drug -> Gene interaction
    # ~ dg = "../data/drug_gene_interactions.csv"
    # ~ dr_gn = pd.read_csv(dg)
    # ~ if NSAMPLE >0:
        # ~ dr_gn = dr_gn.sample(NSAMPLE)
    
    # ~ cls = ["gene_name","drug_claim_name","drug_claim_primary_name","drug_name","drug_concept_id"]
    # ~ dr_gn = dr_gn[cls]
    
    
    
    # ~ print("Drug -> Gene interaction")
    # ~ for ind,rw in tqdm(dr_gn.iterrows()):
        # ~ gn = str(rw["gene_name"])
        # ~ drs = list(rw[["drug_claim_name","drug_claim_primary_name","drug_name"]])
        # ~ drs = [str(dr) for dr in drs]
        # ~ drs = list(set([dr.lower() for dr in drs if dr !="nan"]))
        
        # ~ if gn !="nan" and len(drs)>0:
            # ~ for oc in ocm:
                # ~ if oc[1] in drs:
                    # ~ G.add_edge(oc[0],gn,label="targets")
                    # ~ G.nodes[gn]["labels"] = "_Gene"
                    # ~ G.nodes[gn]["name"] = gn

    
    # ~ ##03 Drug -> Protein interaction
    # ~ dp = "../data/drug_target_interaction.csv"
    # ~ dr_pt = pd.read_csv(dp)
    # ~ if NSAMPLE >0:
        # ~ dr_pt = dr_pt.sample(NSAMPLE)
    
    # ~ cpls = ["DRUG_NAME","ACCESSION"]
    # ~ dr_pt = dr_pt[cpls]
    
    
    
    # ~ print("Drug -> Protein interaction")
    # ~ for ind,rw in tqdm(dr_pt.iterrows()):
        # ~ drr = str(rw["DRUG_NAME"]).lower()
        # ~ pts = str(rw["ACCESSION"])
        # ~ pts = pts.split("|")
        # ~ pts = [pt for pt in pts if pt !="nan"]
        
        # ~ if drr !="nan" and len(pts)>0:
            # ~ for oc in ocm:
                # ~ if oc[1] ==drr:
                    # ~ for pt in pts:
                        # ~ G.add_edge(oc[0],pt,label="acts_on")
                        # ~ G.nodes[pt]["labels"] = "_Protein"
                        # ~ G.nodes[pt]["name"] = pt





# ~ ATC = True
    
# ~ if ATC:
    # ~ ##04 ATC Ontology annotation
    # ~ fg = "/home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/ALPHA_GENOME/Ontology_parsers/out/ATC/ATC.graphml"
    # ~ AT  = nx.read_graphml(fg)
    
    # ~ # Re-name
    # ~ for nd in AT.nodes:
        # ~ att = AT.nodes[nd]
        # ~ att["name"] = att.pop("label")
    # ~ for ed in AT.edges:
        # ~ att = AT.edges[ed]
        # ~ att["label"] = att.pop("type")
    
    # ~ # Update

    # ~ nx.set_node_attributes(AT, "Medical_concept", "labels")
    
    
    # ~ drg_nd = [nd for nd in G.nodes if G.nodes[nd]["labels"] in ["Compound","Drug"]]
    # ~ drg_nd = [(nd,G.nodes[nd]["name"].lower()) for nd in G.nodes if G.nodes[nd]["labels"] in ["Compound"]]
    
    
    # ~ GAT = nx.compose(G,AT)
    # ~ print("ATC Ontology annotation")
    # ~ for d in tqdm(drg_nd):
        # ~ for at in AT.nodes:
            # ~ if d[1].lower()== AT.nodes[at]["name"].lower():
                # ~ GAT.add_edge(d[0],at,label="onto_xref")
            # ~ elif "generic" in G.nodes[d] and  G.nodes[d]["generic"].lower()== AT.nodes[at]["name"].lower():
                # ~ GAT.add_edge(d[0],at,label="onto_xref")
    # ~ G = GAT

            
    



