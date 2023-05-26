LOAD CSV WITH HEADERS FROM "file:///smpl1_DRKG_nodes.csv" AS line
MERGE (e:line.labels {id:line.ID})
ON CREATE SET e.name=line.name
RETURN COUNT(e) AS c;

LOAD CSV WITH HEADERS FROM "file:///IMPORTDIR/ENTITY_has_parent.tsv" AS line
FIELDTERMINATOR '\t'
MATCH (e1:ENTITY{id:line.START_ID})
MATCH (e2:ENTITY{id:line.END_ID})
MERGE (e1)-[r:HAS_PARENT]->(e2)
RETURN COUNT(r) AS c;



# Clean indexes
CALL apoc.schema.assert({},{},true) YIELD label, key
RETURN *


# Import Graphml
CALL apoc.import.graphml("/import/MESH.graphml",{readLabels:TRUE})

##= Merge nodes by attribute
MATCH (n)
WITH n.id AS id, COLLECT(n) AS nodelist, COUNT(*) AS count
WHERE count > 1
CALL apoc.refactor.mergeNodes(nodelist,{
  properties:"combine",
  mergeRels:true
})
YIELD node
RETURN node; 

MATCH (n)
WITH n.id AS id, COLLECT(n) AS nodelist, COUNT(*) AS count
WHERE count > 1
CALL apoc.refactor.mergeNodes(nodelist,{
  properties:"combine",
})
YIELD node
RETURN node;


##= Count labels

MATCH (n) RETURN distinct labels(n), count(*) AS cnt
ORDER BY cnt DESC


## Get neighbors and rank resulting subgraph by deegree ON RESULT SUBGRAPH
MATCH (n1:Node{uuid: "n1_34"})-()-[r]-(n2:Node)
RETURN n2.uuid AS uuid, count(r) AS n
ORDER BY n DESC



## Change data type



## ALPHA10X query
MATCH (c:Startup) -[r:is_associated_to]-> (n:Technology {name:"Artificial intelligence"})
where c.country = "United States"
return c.name, c.rank
order by c.rank DESC
SKIP 25
LIMIT 25
