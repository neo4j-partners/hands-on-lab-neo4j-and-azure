"""
Temporary script to explore Neo4j database schema and relationships
"""
import sys
sys.path.insert(0, 'new-workshops/solutions')

from neo4j import GraphDatabase
from config import Neo4jConfig


def explore_database():
    """Explore the database to understand the schema."""
    neo4j_config = Neo4jConfig()
    driver = GraphDatabase.driver(
        neo4j_config.uri,
        auth=(neo4j_config.username, neo4j_config.password)
    )

    try:
        with driver.session() as session:
            print("="*60)
            print("1. ALL NODE LABELS")
            print("="*60)
            result = session.run("""
                CALL db.labels()
                YIELD label
                RETURN label
                ORDER BY label
            """)
            for record in result:
                print(f"  - {record['label']}")

            print("\n" + "="*60)
            print("2. ALL RELATIONSHIP TYPES")
            print("="*60)
            result = session.run("""
                CALL db.relationshipTypes()
                YIELD relationshipType
                RETURN relationshipType
                ORDER BY relationshipType
            """)
            for record in result:
                print(f"  - {record['relationshipType']}")

            print("\n" + "="*60)
            print("3. COMPANY NODES (with properties)")
            print("="*60)
            result = session.run("""
                MATCH (c:Company)
                RETURN c.name as name, labels(c) as labels, properties(c) as props
                LIMIT 10
            """)
            for record in result:
                print(f"\nName: {record['name']}")
                print(f"  Labels: {record['labels']}")
                print(f"  Properties: {record['props']}")

            print("\n" + "="*60)
            print("4. PRODUCT NODES (with properties)")
            print("="*60)
            result = session.run("""
                MATCH (p:Product)
                RETURN p.name as name, labels(p) as labels, properties(p) as props
                LIMIT 10
            """)
            for record in result:
                print(f"\nName: {record['name']}")
                print(f"  Labels: {record['labels']}")
                print(f"  Properties: {record['props']}")

            print("\n" + "="*60)
            print("5. ALL RELATIONSHIPS FROM COMPANY NODES")
            print("="*60)
            result = session.run("""
                MATCH (c:Company)-[r]->(target)
                RETURN c.name as company, type(r) as rel_type, labels(target) as target_labels,
                       target.name as target_name
                LIMIT 20
            """)
            count = 0
            for record in result:
                print(f"  {record['company']} -[{record['rel_type']}]-> {record['target_labels']} ({record['target_name']})")
                count += 1
            if count == 0:
                print("  No relationships found from Company nodes")

            print("\n" + "="*60)
            print("6. ALL RELATIONSHIPS TO PRODUCT NODES")
            print("="*60)
            result = session.run("""
                MATCH (source)-[r]->(p:Product)
                RETURN labels(source) as source_labels, source.name as source_name,
                       type(r) as rel_type, p.name as product
                LIMIT 20
            """)
            count = 0
            for record in result:
                print(f"  {record['source_labels']} ({record['source_name']}) -[{record['rel_type']}]-> {record['product']}")
                count += 1
            if count == 0:
                print("  No relationships found to Product nodes")

            print("\n" + "="*60)
            print("7. SAMPLE PATHS INVOLVING 'Apple'")
            print("="*60)
            result = session.run("""
                MATCH path = (n)-[r]-(m)
                WHERE n.name CONTAINS 'Apple' OR m.name CONTAINS 'Apple'
                RETURN n.name as node1, labels(n) as labels1, type(r) as rel,
                       m.name as node2, labels(m) as labels2
                LIMIT 20
            """)
            for record in result:
                print(f"  {record['labels1']} ({record['node1']}) -[{record['rel']}]- {record['labels2']} ({record['node2']})")

            print("\n" + "="*60)
            print("8. SAMPLE PATHS INVOLVING 'iPhone'")
            print("="*60)
            result = session.run("""
                MATCH path = (n)-[r]-(m)
                WHERE n.name CONTAINS 'iPhone' OR m.name CONTAINS 'iPhone'
                RETURN n.name as node1, labels(n) as labels1, type(r) as rel,
                       m.name as node2, labels(m) as labels2
                LIMIT 20
            """)
            for record in result:
                print(f"  {record['labels1']} ({record['node1']}) -[{record['rel']}]- {record['labels2']} ({record['node2']})")

            print("\n" + "="*60)
            print("9. COMPANY TO PRODUCT PATHS (any relationship)")
            print("="*60)
            result = session.run("""
                MATCH path = (c:Company)-[*1..2]-(p:Product)
                WHERE c.name CONTAINS 'Apple'
                RETURN c.name as company,
                       [r in relationships(path) | type(r)] as rel_types,
                       p.name as product
                LIMIT 10
            """)
            count = 0
            for record in result:
                print(f"  {record['company']} -{record['rel_types']}-> {record['product']}")
                count += 1
            if count == 0:
                print("  No paths found between Company and Product nodes")

            print("\n" + "="*60)
            print("10. SCHEMA VISUALIZATION")
            print("="*60)
            result = session.run("""
                CALL db.schema.visualization()
            """)
            for record in result:
                nodes = record['nodes']
                relationships = record['relationships']
                print(f"\nNodes in schema: {len(nodes)}")
                for node in nodes:
                    print(f"  - {node}")
                print(f"\nRelationships in schema: {len(relationships)}")
                for rel in relationships:
                    print(f"  - {rel}")

    finally:
        driver.close()


if __name__ == "__main__":
    explore_database()
