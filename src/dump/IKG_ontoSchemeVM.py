
import glob
import os
import pandas as pd
from py2neo import Graph
import time
from collections import OrderedDict
from pprint import pprint



def SSH_get_files(PATH, host = "20.73.5.87",name="alpha10x",key_filename="neo4jvm.pem"):
    import paramiko
    client = paramiko.SSHClient()
    # Create a 'host_keys' object and load
    # our local known hosts  
    host_keys = client.load_system_host_keys()
    # ~ client.connect(host, username=name, password=pwd)
    client.connect(host, username=name, key_filename=key_filename)
    
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


#### =============================================

queryMap = """
MATCH (n:FROM_TYPE)
SET n:TO_TYPE;"""

queryIND = """
CREATE INDEX IF NOT EXISTS
FOR (n:TO_TYPE)
ON (n.id);
"""


TO_FROM = OrderedDict()

# Fist level grouping
TO_FROM["Company"] = ["Startup","Private","Public"]
TO_FROM["Technical_topic"] = ["Technology","Domain","Scientific_concept"]
TO_FROM["Medical_topic"] = ["Medical_term","Drug","Disease","Protein"]

# Second level grouping
TO_FROM["Organization"] = ["Company","Fund"]
TO_FROM["Topic"] = ["Medical_topic","Technical_topic"]

# Last grouping
TO_FROM["Node"] = ["Topic","Organization","Person","Sdg","Scientific_paper"]






# ~ graph = Graph("bolt://192.168.1.30:11009", auth=("neo4j", "lskg_alpha10x"), name="ikg")
graph = Graph("bolt://20.73.5.87:7687", auth=("neo4j", "letmein10X!"), name="ikg")
# ~ graph = Graph("bolt://localhost:7687", auth=("neo4j", "Knopik@82"))



for k, vl in TO_FROM.items():
    #print(k,v)
    for v in vl:
        qrm = queryMap.replace("FROM_TYPE",v).replace("TO_TYPE",k)
        print(qrm)
        graph.run(qrm)
    qrin = queryIND.replace("TO_TYPE",k)
    print(qrin)
    graph.run(qrin)


pprint(TO_FROM)
# ~ end = time.time()
# ~ print("Total time of ingestion: ", end - start)




cnt_nodes =  graph.run("MATCH (n) RETURN count(n)")
cnt_edges =  graph.run("MATCH ()-->() RETURN count(*)")

print("Number of nodes ", cnt_nodes)
print("Number of edges ", cnt_edges)

stat_edges  = graph.run("CALL apoc.meta.stats()").to_data_frame()

stat_nd = stat_edges.iloc[0]["labels"]
stat_rel = stat_edges.iloc[0]["relTypesCount"]



print("\n Nodes stat ")
print("-"*50)
pprint(stat_nd)

print("\n Edges stat ")
print("-"*50)
pprint(stat_rel)



