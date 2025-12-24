from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# Add paper and author relationship
def add_paper(title: str, author: str):
    with driver.session() as session:
        session.run(
            """
            MERGE (p:Paper {title: $title})
            MERGE (a:Author {name: $author})
            MERGE (a)-[:WROTE]->(p)
            """,
            title=title,
            author=author
        )

# Add citation relationship (future use)
def add_citation(source_title: str, cited_title: str):
    with driver.session() as session:
        session.run(
            """
            MERGE (p1:Paper {title: $source})
            MERGE (p2:Paper {title: $target})
            MERGE (p1)-[:CITES]->(p2)
            """,
            source=source_title,
            target=cited_title
        )

# Query papers by author
def get_papers_by_author(author: str):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (a:Author {name: $author})-[:WROTE]->(p:Paper)
            RETURN p.title AS title
            """,
            author=author
        )
        return [record["title"] for record in result]

