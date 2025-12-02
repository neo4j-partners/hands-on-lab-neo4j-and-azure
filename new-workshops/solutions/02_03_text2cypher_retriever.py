"""
Text2Cypher Retriever Demo

This workshop demonstrates converting natural language queries to Cypher
using Text2CypherRetriever from neo4j-graphrag-python.

Run with: uv run python solutions/01_03_text2cypher_retriever.py
"""

from typing import Final

from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import Text2CypherRetriever
from neo4j_graphrag.schema import get_schema

from config import get_llm, get_neo4j_driver

# Custom prompt to ensure generated Cypher queries are limited
TEXT2CYPHER_PROMPT: Final[str] = """Task: Generate a Cypher statement to query a graph database.

Instructions:
- Use only the provided relationship types and properties in the schema.
- Do not use any other relationship types or properties that are not provided.
- Always add LIMIT 20 to the end of your query to restrict results.

Schema:
{schema}

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{query_text}"""


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
        custom_prompt=TEXT2CYPHER_PROMPT,
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
    response = rag.search(query, retriever_config={"top_k": 5}, return_context=True)

    print(f"Number of results returned: {len(response.retriever_result.items)}\n")
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
