

# ~ from neo4j import GraphDatabase

class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


# ~ if __name__ == "__main__":
    # ~ greeter = HelloWorldExample("bolt://192.168.1.30:11009", "neo4j", "lskg_alpha10x")
    # ~ greeter.print_greeting("hello, world")
    # ~ greeter.close()

from py2neo import Graph
graph = Graph("bolt://192.168.1.30:11009", auth=("neo4j", "lskg_alpha10x"))
# ~ graph = Graph("bolt://localhost:7687", auth=("neo4j", "Knopik@82"))

# ~ rt  = graph.run("UNWIND range(1, 3) AS n RETURN n, n * n as n_sq")
# ~ rt  = graph.run("MATCH (n) RETURN distinct labels(n), count(*) AS cnt ORDER BY cnt DESC").to_data_frame()
# ~ stat_edges  = graph.run("MATCH ()-[r]-() RETURN distinct type(r), count(*) AS cnt ORDER BY cnt DESC").to_data_frame()
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
