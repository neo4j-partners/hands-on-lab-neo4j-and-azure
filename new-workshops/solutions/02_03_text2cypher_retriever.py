"""
Text2Cypher Retriever Demo

This workshop demonstrates converting natural language queries to Cypher
using Text2CypherRetriever from neo4j-graphrag-python.

Run with: uv run python solutions/01_03_text2cypher_retriever.py
"""

from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.schema import get_schema

from config import get_llm, get_neo4j_driver


def create_text2cypher_retriever(driver, llm) -> Text2CypherRetriever:
    """Create a Text2CypherRetriever."""
    schema = get_schema(driver)
    print("Database Schema:")
    print(schema)
    print()

    return Text2CypherRetriever(
        driver=driver,
        llm=llm,
        neo4j_schema=schema,
    )


def demo_cypher_generation(retriever: Text2CypherRetriever, query: str) -> None:
    """Demo Cypher generation and execution."""
    print(f"\n{'=' * 60}")
    print(f"--- Cypher Generation Demo ---")
    print(f"Query: {query}\n")

    result = retriever.get_search_results(query)

    print(f"Generated Cypher: {result.metadata['cypher']}")
    print(f"\nResults:")
    for record in result.records:
        print(f"  {record}")


def demo_rag_search(llm, retriever: Text2CypherRetriever, query: str) -> None:
    """Demo RAG with text2cypher."""
    print(f"\n{'=' * 60}")
    print(f"--- RAG with Text2Cypher Demo ---")
    print(f"Query: {query}\n")

    rag = GraphRAG(llm=llm, retriever=retriever)
    response = rag.search(query, return_context=True)

    print(f"Answer: {response.answer}")
    print(f"\nGenerated Cypher: {response.retriever_result.metadata['cypher']}")


def main():
    """Run text2cypher retriever demos."""
    with get_neo4j_driver() as driver:
        llm = get_llm()
        retriever = create_text2cypher_retriever(driver, llm)

        # Demo 1: Direct Cypher generation
        demo_cypher_generation(retriever, "What companies are owned by BlackRock Inc.")

        # Demo 2: RAG search
        demo_rag_search(llm, retriever, "Who are the asset managers?")

        # Demo 3: Another RAG example
        demo_rag_search(llm, retriever, "Summarise the products mentioned in the company filings.")


if __name__ == "__main__":
    main()


# Example queries to try:
# - What companies are owned by BlackRock Inc.
# - Who are the asset managers?
# - Summarise the products mentioned in the company filings.
# - How many risk factors does Apple face?
# - What companies mention cybersecurity in their filings?
