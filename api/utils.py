from neo4j import GraphDatabase
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("uri")
user = os.getenv("username")
password = os.getenv("password")


def get_driver():
    return GraphDatabase.driver(uri, auth=(user, password))


def upload_csv_to_neo4j(file_path: str, clear_database: bool = True):
    driver = get_driver()
    with driver.session() as session:
        df = pd.read_csv(file_path)
        # clear the database
        if clear_database:
            session.run("MATCH (n) DETACH DELETE n")
        # populate the database with the csv data
        for index, row in df.iterrows():
            query = """             
                MERGE(s1:Station {name: $from_station})
                MERGE(s2:Station {name: $to_station})
                MERGE (s1)-[:ROUTE {cost: $cost}]->(s2);
                """
            session.run(
                query,
                from_station=row["from_name"],
                to_station=row["to_name"],
                cost=row["estimated_cost"],
            )


def query_neo4j(s1: str, s2: str):
    driver = get_driver()
    with driver.session() as session:
        query = """
            MATCH (s1:Station {name: $from_station})-[r:ROUTE]->(s2:Station {name: $to_station})
            RETURN s1.name AS from_station, s2.name AS to_station, r.cost AS cost
        """
        result = session.run(query, from_station=s1, to_station=s2)
        return result.data()
