#!pip install azure-storage-blob
from azure.storage.blob import ContainerClient, BlobClient, BlobServiceClient
import pandas as pd

class Datalake:
    __URL = 'https://stalpha10xlaboratory.blob.core.windows.net/'
    __SHARED_ACCESS_KEY = '?sv=2020-08-04&ss=b&srt=sco&sp=rwdlacx&se=2021-12-31T00:32:03Z&st=2021-10-07T15:32:03Z&spr=https&sig=b2ywBjtwca1Dre7a9ahSjEspoP8Y5Ldz%2BWfDFylikrQ%3D'
    def list_all_containers(self):
        blob_service_client = BlobServiceClient(account_url=self.__URL, credential=self.__SHARED_ACCESS_KEY)
        all_containers = blob_service_client.list_containers(include_metadata=True)
        for container in all_containers:
            print(container['name'])
    def list_all_directories(self, container_name):
        blob_service_client = BlobServiceClient(account_url=self.__URL, credential=self.__SHARED_ACCESS_KEY)
        container_client = blob_service_client.get_container_client(container_name)
        for file in container_client.walk_blobs(delimiter='/'):
            print(file.name)    
    def list_all_blobs(self, container_name):
        blob_service_client = BlobServiceClient(account_url=self.__URL, credential=self.__SHARED_ACCESS_KEY)
        container_client = blob_service_client.get_container_client(container_name)
        try:
            for blob in container_client.list_blobs():
                print("Found blob: ", blob.name)
        except ResourceNotFoundError:
                print("Container not found.") 
    def get_all_files(self, container_name, prefix):
        blobs = []
        blob_service_client = BlobServiceClient(account_url=self.__URL, credential=self.__SHARED_ACCESS_KEY)
        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs(prefix)
        for blob in blob_list:
            a = blob.name.rsplit('/', 1)[-1]
            blobs.append(a)
        return blobs[1:]
    def get_blob_urls(self, container_name, prefix):
        urls = []
        blob_service_client = BlobServiceClient(account_url=self.__URL, credential=self.__SHARED_ACCESS_KEY)
        container_client = blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs(prefix)
        for blob in blob_list:
            a = f"https://stalpha10xlaboratory.blob.core.windows.net/{container_name}/{blob.name}{self.__SHARED_ACCESS_KEY}"
            urls.append(a)
        return urls[1:]
    def read_csv_file(self, container_name, path):
        blob_service_client = BlobServiceClient(account_url=self.__URL, credential=self.__SHARED_ACCESS_KEY)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(path)
        read = blob_client.download_blob().readall()
        df = pd.read_csv(io.StringIO(read.decode('utf-8')))
        return df



DT = Datalake()

lurl = DT.get_blob_urls('kuanysh', 'LSKG/vertices/')
fnm  = DT.get_all_files('kuanysh', 'LSKG/vertices/')

hd = []

for i,lk in enumerate(lurl[:2]):

    a = pd.read_csv(lk, nrows=2).columns.to_list()
    
    hd.append((fnm[i],lk,a))
    print(fnm[i],lk,a)











import glob
import os
import pandas as pd
from py2neo import Graph
import time




#### =============================================
NODES = True
EDGES = False

# WITH line LIMIT 10000
queryN = """
CREATE CONSTRAINT ON (e:ENTITY) ASSERT e.id IS UNIQUE;
CREATE INDEX ON :ENTITY(name);
USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "FILENAME" AS line
MERGE (e:ENTITY {id:line.id})
ON_CREATE_SET
RETURN COUNT(e) AS c
"""

queryE = """
USING PERIODIC COMMIT 10000
LOAD CSV WITH HEADERS FROM "file:///FILENAME" AS line
MATCH (e1:ENTITY1 {id:line.source})
MATCH (e2:ENTITY2 {id:line.target})
MERGE (e1)-[r:RELATION]->(e2)
RETURN COUNT(r) AS c
"""








# ~ graph = Graph("bolt://192.168.1.30:11009", auth=("neo4j", "lskg_alpha10x"), name="ikg")
graph = Graph("bolt://20.73.5.87:7687", auth=("neo4j", "letmein10X!"), name="test")
# ~ graph = Graph("bolt://localhost:7687", auth=("neo4j", "Knopik@82"))

# ~ PATH = "/var/lib/neo4j/import/"
# ~ PATH_I = "/"



# ~ PATH_NODES = PATH+"nodes/"
# ~ PATH_EDGES = PATH+"edges/"
# ~ PATH_NODES_I = PATH+"nodes/"
# ~ PATH_EDGES_I = PATH+"edges/"

TO_INT   = ["technologies_count", "companies_count","amount"]
TO_FLOAT = ["rank","weight"]
TRANS = list(set(TO_INT)|set(TO_FLOAT))



start = time.time()



if NODES:

    # ~ flst = SSH_get_files(PATH_NODES)
    # ~ flst = glob.glob(PATH_LOC_NODES+"*.csv")


    for fn,lk,cln in hd:

        # ~ fn = fn.replace(PATH,"/")
        ENT = os.path.basename(fn).split(".")[0].capitalize()


        bn = ["label","connections_count","id"]
        cln = [c for c in cln if c not in bn]

        OCS = [f"e.{c}=line.{c}" for c in cln if c not in TRANS]
        TI = [f"e.{c}=toInteger(line.{c})" for c in cln if c in TO_INT ]
        TF = [f"e.{c}=toFloat(line.{c})" for c in cln if c in TO_FLOAT ]
        
        OCS = OCS + TI +TF
        OCS = "ON CREATE SET "+", ".join(OCS)


        QR = queryN.replace("FILENAME",lk).replace("ENTITY",ENT).replace("ON_CREATE_SET",OCS)
        QRL = QR.split(";")


        
        print(f"Ingesting {ENT}")
        print("-"*40)
        for qr in QRL:
            print(qr)
            rt  = graph.run(qr)











# ~ lurl = DT.read_csv_file(container_name="kuanysh", path= "LSKG/LSKG_edges/disease-is_parent_of-disease.csv")
