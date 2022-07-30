import os
from typing import Optional
from neo4j import GraphDatabase, Driver, basic_auth

from src.settings import SETTINGS


class Database:
    driver: Driver = None

    @classmethod
    def connect(cls):
        try:
            cls.driver = GraphDatabase.driver(
                uri=os.getenv('NEO4J_URI', SETTINGS.NEO4J.URI),
                auth=basic_auth(
                    os.getenv('NEO4J_USERNAME', SETTINGS.NEO4J.USERNAME),
                    os.getenv('NEO4J_PASSWORD', SETTINGS.NEO4J.PASSWORD),
                )
            )
            print('Database connected')
        except Exception as ex:
            print(ex)

    @classmethod
    def disconnect(cls):
        if cls.driver:
            cls.driver.close()
        print('Database disconnected')

    @classmethod
    def read(cls, query: str):
        with cls.driver.session(
            database=os.getenv('NEO4J_DATABASE', SETTINGS.NEO4J.DATABASE)
        ) as session:
            return session.read_transaction(lambda tx: list(tx.run(query)))

    @classmethod
    def write(cls, statement: str):
        with cls.driver.session(
            database=os.getenv('NEO4J_DATABASE', SETTINGS.NEO4J.DATABASE)
        ) as session:
            session.write_transaction(lambda tx: tx.run(statement))

    @classmethod
    def read_from_file(
        cls,
        file_path: str,
        params: Optional[dict] = None
    ):
        infile = open(file_path, 'r')
        query = infile.read().strip()

        if params:
            for (pk, pv) in params.items():
                query = query.replace(str(pk), str(pv))

        records = cls.read(query)
        infile.close()
        return records

    @classmethod
    def count_nodes(cls, label: Optional[str] = None):
        """ Count the nodes with the given label otherwise all nodes. """

        query = \
            f"MATCH (n{f':{label}' if label else ''}) RETURN COUNT(n) AS count;"
        return cls.read(query)[0]['count']

    @classmethod
    def count_relationships(
        cls,
        rel_type: Optional[str] = None,
        is_directed: Optional[bool] = True
    ):
        """ Count the relationships with the given type and direction. """

        direction = '->' if is_directed else '-'
        rtype = f'[:{rel_type}]' if rel_type else ''
        query = f'MATCH ()-{rtype}{direction}() RETURN COUNT(*) AS count;'
        return cls.read(query)[0]['count']
