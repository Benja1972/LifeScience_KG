## Query ONE ==============================================================================================
g.V().has("id", "9a53b9c4-3ce7-4bd2-a39a-760f8c457d31").union( 
	__.in('relates_to', 'is_parent_of').hasLabel('domain').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('domain').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.in('relates_to', 'is_parent_of').hasLabel('technology').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('technology').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.in('relates_to', 'is_parent_of').hasLabel('application').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('application').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('relates_to', 'is_parent_of').hasLabel('domain').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('domain').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.in('relates_to', 'is_parent_of').hasLabel('technology').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('technology').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.in('relates_to', 'is_parent_of').hasLabel('application').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('application').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('relates_to').hasLabel('patent').range(0, 10), 
	__.out('owns').hasLabel('patent').range(0, 10), 
	__.in('relates_to').hasLabel('scientific_paper').range(0, 10), 
	__.out('owns').hasLabel('scientific_paper').range(0, 10), 
	__.in('is_executive_in', 'is_board_member_of', 'is_founder_of').hasLabel('person').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('relates_to').hasLabel('patent').range(0, 10), 
	__.out('owns').hasLabel('patent').range(0, 10), 
	__.in('relates_to').hasLabel('scientific_paper').range(0, 10), 
	__.out('owns').hasLabel('scientific_paper').range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('fund').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('is_associated_to', 'acquired', 'owns', 'invested_in', 'works_in', 'is_subsidiary_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.out('acquired', 'is_executive_in', 'is_founder_of', 'invested_in', 'is_board_member_of').hasLabel('startup', 'public', 'private').where(values("rank")).order().by("rank", incr).range(0, 10), 
	__.in('relates_to', 'is_parent_of').hasLabel('domain').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('domain').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.in('relates_to', 'is_parent_of').hasLabel('technology').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('technology').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.in('relates_to', 'is_parent_of').hasLabel('application').where(values("rank")).order().by("rank", decr).range(0, 10), 
	__.out('is_associated_to', 'is_parent_of', 'works_in').hasLabel('application').where(values("rank")).order().by("rank", decr).range(0, 10)
).dedup()

# ------------------
MATCH (n)
WHERE labels(n) in [['Startup'], ['Private'],["Public"]]
SET n:Company
RETURN count(n)


# ------------------
CREATE INDEX ON :Company(id)


# ------------------
MATCH (n {id:"ac2cbcd2-e23c-431f-b48d-627da51dae7a"})
CALL {
	WITH n 
	MATCH (n)-[]->(t:Technology)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)<-[]-(t:Technology)
	RETURN t order by t.rank desc limit 10

	UNION
	WITH n 
	MATCH (n)-[]->(t:Domain)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)<-[]-(t:Domain)
	RETURN t order by t.rank desc limit 10

	
	UNION
	WITH n 
	MATCH (n)-[]->(t:Fund)
	RETURN t order by t.rank asc limit 10
	
	
	UNION
	WITH n 
	MATCH (n)<-[]-(t:Fund)
	RETURN t order by t.rank asc limit 10

	
	UNION
	WITH n 
	MATCH (n)-[]->(t:Scientific_paper)
	RETURN t order by t.rank limit 10
	
	UNION
	WITH n 
	MATCH (n)<-[]-(t:Scientific_paper)
	RETURN t order by t.rank limit 10

	
	UNION
	WITH n 
	MATCH (n)-[]->(t:Company)
	RETURN t order by t.rank asc limit 10
	
	UNION
	WITH n 
	MATCH (n)<-[]-(t:Company)
	RETURN t order by t.rank asc limit 10

}

RETURN t
# ------------------
MATCH (n:Node {id:"ac2cbcd2-e23c-431f-b48d-627da51dae7a"})
CALL {
	WITH n 
	MATCH (n)-[]-(t:Technology)
	RETURN t order by t.rank desc limit 10
	

	UNION
	WITH n 
	MATCH (n)-[]-(t:Domain)
	RETURN t order by t.rank desc limit 10


	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Fund)
	RETURN t order by t.rank asc limit 10
	

	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Scientific_paper)
	RETURN t order by t.rank limit 10


	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Company)
	RETURN t order by t.rank asc limit 10


}

RETURN t





## QUERY TWO ==============================================================================================
g.V().has("id", "ac2cbcd2-e23c-431f-b48d-627da51dae7a").both()
.union(
	__.has("label", within(["technology"])).where(values("rank")).order().by("rank", incr).range(0, 10),
	__.has("label", within(["domain"])).where(values("rank")).order().by("rank", incr).range(0, 10),
	__.has("label", within(["scientific_concept"])).where(values("rank")).order().by("rank", incr).range(0, 10),
	__.has("label", within(["private", "public", "startup"])).where(values("rank")).order().by("rank", incr).range(0, 10),
	__.has("label", within(["scientific_paper"])).where(values("rank")).order().by("rank", incr).range(0, 10),
	__.has("label", within(["scientific_paper", "medical_term", "disease", "drug", "protein"])).range(0, 10)
).dedup()






MATCH (n:Node {id:"ac2cbcd2-e23c-431f-b48d-627da51dae7a"})
CALL {
	WITH n 
	MATCH (n)-[]-(t:Technology)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Scientific_concept)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Domain)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Scientific_paper)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t)
	WHERE labels(t) in [['Startup'], ['Private'],["Public"]]
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t)
	WHERE labels(t) in [["Medical_term"],["Disease"],["Drug"],["Protein"]]
	RETURN t order by t.rank desc limit 10
}

RETURN t

TOTAL: 1155 ms



MATCH (n:Domain {id:"ac2cbcd2-e23c-431f-b48d-627da51dae7a"})
CALL {
	WITH n 
	MATCH (n)-[]-(t:Technology)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Scientific_concept)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Scientific_papert)
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t)
	WHERE labels(t) in [['Startup'], ['Private'],["Public"]]
	RETURN t order by t.rank desc limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t)
	WHERE labels(t) in [["Medical_term"],["Disease"],["Drug"],["Protein"]]
	RETURN t order by t.rank desc limit 10
}

RETURN t

TOTAL: 83 ms

MATCH (n:Node {id:"ac2cbcd2-e23c-431f-b48d-627da51dae7a"})
CALL {
	WITH n 
	MATCH (n)-[]-(t:Technology)
	RETURN t order by t.rank limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Scientific_concept)
	RETURN t order by t.rank limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t:Scientific_papert)
	RETURN t order by t.rank limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t)
	WHERE labels(t) in [['Startup'], ['Private'],["Public"]]
	RETURN t order by t.rank limit 10
	
	UNION
	WITH n 
	MATCH (n)-[]-(t)
	WHERE labels(t) in [["Medical_term"],["Disease"],["Drug"],["Protein"]]
	RETURN t order by t.rank limit 10
}

RETURN t

TOTAL 215 ms



## QUERY THREE ==============================================================================================
g.V().has("id", within(['b2e752d0-0e64-41ce-968b-189b61e6f486', '46da40c4-5bc1-4a75-a485-358263a5c027'])).both().has("label", within(['technology', 'person', 'fund', 'application', 'domain', 'private', 'public', 'startup'])).dedup().where(values("rank")).order().by("rank", incr).limit(10).values("id")

this query  gets all the nodes connected (both in and out) to given list of ids (here 'b2e752d0-0e64-41ce-968b-189b61e6f486', '46da40c4-5bc1-4a75-a485-358263a5c027'), ranks them by rank and gets top 10. This query is very heavy and might sometimes fail






MATCH (n1:Technology {id:'b2e752d0-0e64-41ce-968b-189b61e6f486'})
MATCH (n2:Technology {id:'46da40c4-5bc1-4a75-a485-358263a5c027'})

CALL {
	WITH n1
	MATCH (n1)-[]-(p)
	RETURN p
	
	UNION 
	WITH n2
	MATCH (n2)-[]-(p)
	RETURN p
}
RETURN p  ORDER BY p.rank LIMIT 10

76 ms
#------------------------------

MATCH (n1:Node {id:'b2e752d0-0e64-41ce-968b-189b61e6f486'})
MATCH (n2:Node {id:'46da40c4-5bc1-4a75-a485-358263a5c027'})

CALL {
	WITH n1
	MATCH (n1)-[]-(p)
	RETURN p
	
	UNION 
	WITH n2
	MATCH (n2)-[]-(p)
	RETURN p
}
RETURN p  ORDER BY p.rank LIMIT 10

 84 ms
#------------------------------






## QUERY FOUR ==============================================================================================

g.V().has("id", 
within(['ac2cbcd2-e23c-431f-b48d-627da51dae7a', '6f600a1d-3bb6-410a-ba7f-2ebf6c99ce0c', '17398677-beeb-4ce2-8120-47007a5aef3c', 'c63d0d0b-84c7-4b79-9196-0213eb027357', '8d53d364-406a-48ea-a72e-295141cce569', 'd9c4b256-71ec-4169-88fb-304ac07a7c43', '6a2447ec-ecc4-4e49-9dd6-177c6773a147', '9197a9c0-f882-46ae-ab51-6a7b152d3e2d', 'a3e09aeb-03e5-48b1-8e1c-2d3ba580261c', '7a8c14ae-6cf2-4139-bfe9-740d868b42e5', 'ad25e794-1df9-4d4e-860f-96cd6e7d8e99', '045851e7-74ac-4e67-873b-4252eefa89ed', 'cc7897ef-57d4-42d6-bd80-c41846f723df', 'fdd65a9d-312e-4446-8197-4fef30aca525', '01e2d435-f24c-42bd-b4a9-d111f6b43cb4', '74e7105b-9422-40ae-b6a9-cb17a8db8e5f', 'f80650c4-77da-4e56-94fb-e1930802fb5c', '818910ac-7c4e-4e0c-b428-765c3ec41f30', '588d5e06-bb73-482b-99ca-844d2d181fd8', 'fe259269-edd8-4b03-9524-f6c512a6f1fd', '5df22eb2-26ca-482a-94d9-10bfedfbd9fa', '3169f93d-9821-bb4c-4257-e6b64805977a', 'e22f47cf-3d43-6485-40a2-d08aa4a6989b', '34031ce9-f472-f939-f399-fd6f05451951', '25b3d562-4486-aa35-349c-67866789d9bf', 'cf6d3339-99d3-6ff2-4709-3f071d130750', '95da2158-607a-d69c-1492-f68b01832636', '499ae2f1-1bcf-eeb6-3c55-30bd78788b38', '86bdc2bc-df12-41c2-b0e3-91b5191228fb', '671a1f8e-6226-401c-6e34-08085b4d5cb3', '211cd373-87b6-483a-90b5-d19899084969', '5646b59a-24d1-adc8-9f44-384f4b1f8c67', '65a23d6c-5ffb-66c2-fd09-a9f3b2cb5841', '67d77710-3ed9-46ff-843f-abd533b0a6a7', '7ad11657-573d-5159-6678-0e9a2e5023b8', '2e70f4af-edfc-e9f5-8ce6-72f27f208b20', 'b1d2c2a8-694b-25fc-1d65-8b47ed569f0e', '5f7e8123-7703-520d-8fc4-3268a15ccfb8', '8ab63472-1fc2-9c80-06d7-48ed9fc5bad6', '3d293a4a-e3cc-70cd-205d-2db38a43d14a', '77347697-f336-af8a-a4e2-ae9897c6bfde']))
.outE().where(inV().has("id", 
within(['ac2cbcd2-e23c-431f-b48d-627da51dae7a', '6f600a1d-3bb6-410a-ba7f-2ebf6c99ce0c', '17398677-beeb-4ce2-8120-47007a5aef3c', 'c63d0d0b-84c7-4b79-9196-0213eb027357', '8d53d364-406a-48ea-a72e-295141cce569', 'd9c4b256-71ec-4169-88fb-304ac07a7c43', '6a2447ec-ecc4-4e49-9dd6-177c6773a147', '9197a9c0-f882-46ae-ab51-6a7b152d3e2d', 'a3e09aeb-03e5-48b1-8e1c-2d3ba580261c', '7a8c14ae-6cf2-4139-bfe9-740d868b42e5', 'ad25e794-1df9-4d4e-860f-96cd6e7d8e99', '045851e7-74ac-4e67-873b-4252eefa89ed', 'cc7897ef-57d4-42d6-bd80-c41846f723df', 'fdd65a9d-312e-4446-8197-4fef30aca525', '01e2d435-f24c-42bd-b4a9-d111f6b43cb4', '74e7105b-9422-40ae-b6a9-cb17a8db8e5f', 'f80650c4-77da-4e56-94fb-e1930802fb5c', '818910ac-7c4e-4e0c-b428-765c3ec41f30', '588d5e06-bb73-482b-99ca-844d2d181fd8', 'fe259269-edd8-4b03-9524-f6c512a6f1fd', '5df22eb2-26ca-482a-94d9-10bfedfbd9fa', '3169f93d-9821-bb4c-4257-e6b64805977a', 'e22f47cf-3d43-6485-40a2-d08aa4a6989b', '34031ce9-f472-f939-f399-fd6f05451951', '25b3d562-4486-aa35-349c-67866789d9bf', 'cf6d3339-99d3-6ff2-4709-3f071d130750', '95da2158-607a-d69c-1492-f68b01832636', '499ae2f1-1bcf-eeb6-3c55-30bd78788b38', '86bdc2bc-df12-41c2-b0e3-91b5191228fb', '671a1f8e-6226-401c-6e34-08085b4d5cb3', '211cd373-87b6-483a-90b5-d19899084969', '5646b59a-24d1-adc8-9f44-384f4b1f8c67', '65a23d6c-5ffb-66c2-fd09-a9f3b2cb5841', '67d77710-3ed9-46ff-843f-abd533b0a6a7', '7ad11657-573d-5159-6678-0e9a2e5023b8', '2e70f4af-edfc-e9f5-8ce6-72f27f208b20', 'b1d2c2a8-694b-25fc-1d65-8b47ed569f0e', '5f7e8123-7703-520d-8fc4-3268a15ccfb8', '8ab63472-1fc2-9c80-06d7-48ed9fc5bad6', '3d293a4a-e3cc-70cd-205d-2db38a43d14a', '77347697-f336-af8a-a4e2-ae9897c6bfde'])))
.subgraph("sg").cap("sg")


MATCH (n:Node) WHERE n.id in ['ac2cbcd2-e23c-431f-b48d-627da51dae7a', '6f600a1d-3bb6-410a-ba7f-2ebf6c99ce0c', '17398677-beeb-4ce2-8120-47007a5aef3c', 'c63d0d0b-84c7-4b79-9196-0213eb027357']
WITH collect(n) as nd
UNWIND nd AS n
UNWIND nd AS m
MATCH (n)-[p]->(m)
RETURN n,p,m

2 ms
#------------------------------


MATCH (n1:Node)-[p]->(n2:Node)
WHERE n1.id in ['ac2cbcd2-e23c-431f-b48d-627da51dae7a', '6f600a1d-3bb6-410a-ba7f-2ebf6c99ce0c', '17398677-beeb-4ce2-8120-47007a5aef3c', 'c63d0d0b-84c7-4b79-9196-0213eb027357'] 
AND n2.id in ['ac2cbcd2-e23c-431f-b48d-627da51dae7a', '6f600a1d-3bb6-410a-ba7f-2ebf6c99ce0c', '17398677-beeb-4ce2-8120-47007a5aef3c', 'c63d0d0b-84c7-4b79-9196-0213eb027357'] 
RETURN n1,p,n2

2 ms
#------------------------------



### Intersection 
## https://neo4j.com/developer/kb/performing-match-intersection/
###
WITH ["Artificial intelligence", "Machine learning", "Computer vision"] as names
MATCH (p:Technology)<-[:is_associated_to]-(m:Startup)
WHERE p.name in names
WITH m, size(names) as inputCnt, count(DISTINCT p) as cnt
WHERE cnt = inputCnt
RETURN m


WITH ["Artificial intelligence", "Machine learning", "Computer vision"] as names
MATCH (p:Technology)<-[:is_associated_to]-(m:Startup)
WHERE p.name in names
WITH m, size(names) as inputCnt, count(DISTINCT p) as cnt, collect(p) AS ps
WHERE cnt = inputCnt
RETURN m,ps



