
import glob
import os
import pandas as pd
from py2neo import Graph



def SSH_get_files(PATH, host = "192.168.1.30",name="sergei",pwd="sergei"):
    """
    Function to connect to remote server and get file list and headers
     -  PATH - remote folder to connect  
    """
    import paramiko
    client = paramiko.SSHClient()
    # Create a 'host_keys' object and load
    # our local known hosts  
    host_keys = client.load_system_host_keys()
    client.connect(host, username=name, password=pwd)
    
    # query files
    qr_fls = 'find PATHDIRECTORY -maxdepth 1 -name "*.csv" -type f'.replace("PATHDIRECTORY",PATH)
    stdin, stdout, stderr = client.exec_command(qr_fls)
    fl_lst = [l.strip("\n") for l in list(stdout)]
    
    out_dict = dict()
    # query heads
    for fln in fl_lst: 
        qr_head = 'head -n 1 '+ fln 
        stdin, stdout, stderr = client.exec_command(qr_head)
        hdrs = list(stdout)[0].strip("\n").split(",")
        out_dict[fln]=hdrs

    client.close()
    return out_dict


# Query to ingest nodes
queryN = """
CREATE CONSTRAINT ON (e:ENTITY) ASSERT e.id IS UNIQUE;
CREATE INDEX ON :ENTITY(name);
USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file://FILENAME" AS line
MERGE (e:ENTITY {id:line.id})
ON_CREATE_SET
RETURN COUNT(e) AS c;
"""

# Query to ingest edges
queryE = """
USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///FILENAME" AS line
MATCH (e1:ENTITY1 {id:line.source})
MATCH (e2:ENTITY2 {id:line.target})
MERGE (e1)-[r:RELATION]->(e2)
RETURN COUNT(r) AS c;
"""







# Connect to remote sever 
graph = Graph("bolt://192.168.1.30:11009", auth=("neo4j", "lskg_alpha10x"))
# ~ graph = Graph("bolt://localhost:7687", auth=("neo4j", "Knopik@82"))

# Root path
PATH = "/data/Neo4j/LSKG/neo4j_IKG/"


# Path for nodes and edges
PATH_NODES = PATH+"nodes/"
PATH_EDGES = PATH+"edges/"


NODES = True
if NODES:

    flst = SSH_get_files(PATH_NODES)
    # ~ flst = glob.glob(PATH_LOC_NODES+"*.csv")


    for fn,cln in flst.items():

        # ~ df = pd.read_csv(fn, nrows=10)
        ENT = os.path.basename(fn).split(".")[0].capitalize()


        bn = ["label","connections_count","id"]
        cln = [c for c in cln if c not in bn]

        OCS = [f"e.{c}=line.{c}" for c in cln]
        OCS = "ON CREATE SET "+", ".join(OCS)


        QR = queryN.replace("FILENAME",fn).replace("ENTITY",ENT).replace("ON_CREATE_SET",OCS)
        QRL = QR.split(";")


        
        print(f"Injesting {ENT}")
        print("-"*40)
        for qr in QRL:
            # ~ print(qr)
            rt  = graph.run(qr)


EDGES = True


if EDGES:


    flst =  SSH_get_files(PATH_EDGES)
    # ~ flst = glob.glob(PATH_LOC_EDGES+"*.csv")


    for fn,cln in flst.items():
        E_REL_E = os.path.basename(fn).split(".")[0].split("-")
        ENTITY1 = E_REL_E[0].capitalize()
        REL = E_REL_E[1]
        ENTITY2 = E_REL_E[2].capitalize()


        bn = ["label","id","source","target","source_node","target_node"]
        cln = [c for c in cln if c not in bn]
        if len(cln)>0:
            REL_META = [f"{c}:line.{c}" for c in cln]
            REL_META ="{"+ ", ".join(REL_META) + "}"
            REL+=REL_META


        QRE = queryE.replace("FILENAME",fn).replace("RELATION",REL).replace("ENTITY1",ENTITY1).replace("ENTITY2",ENTITY2)
        
        print(f"Injesting {REL}")
        print("-"*40)
        # ~ print(QRE)
        rt  = graph.run(QRE)



stat_edges  = graph.run("CALL apoc.meta.stats()").to_data_frame()

stat_nd = stat_edges.iloc[0]["labels"]
stat_rel = stat_edges.iloc[0]["relTypesCount"]

from pprint import pprint

print("\n Nodes stat ")
print("-"*50)
pprint(stat_nd)

print("\n Edges stat ")
print("-"*50)
pprint(stat_rel)







