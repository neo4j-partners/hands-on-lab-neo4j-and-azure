"""
Vector Cypher Retriever Demo

This workshop demonstrates combining vector similarity search with custom
Cypher queries for enriched graph context using VectorCypherRetriever.

Run with: uv run python solutions/01_02_vector_cypher_retriever.py
"""

from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import VectorCypherRetriever

from config import get_embedder, get_llm, get_neo4j_driver

# Retrieval query 1: Company + Risk context
COMPANY_RISK_QUERY = """
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(company:Company)-[:FACES_RISK]->(risk:RiskFactor)
RETURN company.name AS company, collect(DISTINCT risk.name)[0..20] AS risks, node.text AS context
"""

# Retrieval query 2: Asset Manager context
ASSET_MANAGER_QUERY = """
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(company:Company)-[:OWNS]-(manager:AssetManager)
RETURN company.name AS company, manager.managerName AS AssetManagerWithSharesInCompany, node.text AS context
"""

# Retrieval query 3: Shared Risks between companies
SHARED_RISKS_QUERY = """
WITH node
MATCH (node)-[:FROM_DOCUMENT]-(doc:Document)-[:FILED]-(c1:Company)
MATCH (c1)-[:FACES_RISK]->(risk:RiskFactor)<-[:FACES_RISK]-(c2:Company)
WHERE c1 <> c2
RETURN
  c1.name AS source_company,
  collect(DISTINCT c2.name) AS related_companies,
  collect(DISTINCT risk.name) AS shared_risks
LIMIT 10
"""


def create_vector_cypher_retriever(
    driver, embedder, retrieval_query: str
) -> VectorCypherRetriever:
    """Create a VectorCypherRetriever with custom retrieval query."""
    return VectorCypherRetriever(
        driver=driver,
        index_name="chunkEmbeddings",
        embedder=embedder,
        retrieval_query=retrieval_query,
    )


def demo_retriever(llm, retriever: VectorCypherRetriever, query: str, description: str) -> None:
    """Demo a retriever with RAG."""
    print(f"\n{'=' * 60}")
    print(f"--- {description} ---")
    print(f"Query: {query}\n")

    rag = GraphRAG(llm=llm, retriever=retriever)
    response = rag.search(query, retriever_config={"top_k": 5}, return_context=True)

    print(f"Answer: {response.answer}")
    print(f"\nContext items retrieved: {len(response.retriever_result.items)}")


def main():
    """Run vector cypher retriever demos with different retrieval queries."""
    with get_neo4j_driver() as driver:
        embedder = get_embedder()
        llm = get_llm()

        # Demo 1: Company + Risk context
        retriever = create_vector_cypher_retriever(driver, embedder, COMPANY_RISK_QUERY)
        demo_retriever(
            llm,
            retriever,
            "What are the top risk factors that Apple faces?",
            "Company Risks",
        )

        # Demo 2: Asset Manager context
        retriever = create_vector_cypher_retriever(driver, embedder, ASSET_MANAGER_QUERY)
        demo_retriever(
            llm,
            retriever,
            "Who are the asset managers most affected by banking regulations?",
            "Asset Managers",
        )

        # Demo 3: Shared Risks between companies
        retriever = create_vector_cypher_retriever(driver, embedder, SHARED_RISKS_QUERY)
        demo_retriever(
            llm,
            retriever,
            "What risks connect major tech companies?",
            "Shared Risks",
        )


if __name__ == "__main__":
    main()


# Example queries to try:
# - What are the top risk factors that Apple faces?
# - Who are the asset managers most affected by banking regulations?
# - What risks connect major tech companies?
# - What companies share cybersecurity risks?
