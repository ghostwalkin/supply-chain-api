from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("uri"),
    auth=(os.getenv("username"), os.getenv("password")),
)


with driver.session() as session:
    # Clear the database
    result = session.run("MATCH (n) RETURN n")
    print(result.data())

    # Create nodes and relationships
driver.close()
