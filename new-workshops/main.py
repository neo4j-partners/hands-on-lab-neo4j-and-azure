#!/usr/bin/env python3
"""
Workshop Solution Runner

Interactive menu to run workshop solutions.

Usage from root directory:
    uv run python new-workshop/main.py          # Interactive menu
    uv run python new-workshop/main.py 4        # Run solution 4 directly
    uv run python new-workshop/main.py A        # Run all from 02_01 onward
"""

import asyncio
import importlib
import sys
from pathlib import Path

# Add solutions directory to path for config imports
sys.path.insert(0, str(Path(__file__).parent / "solutions"))

# Solution definitions: (module_name, title, is_async, entry_func)
SOLUTIONS = [
    ("solutions.01_01_data_loading", "Data Loading Fundamentals", False, "main"),
    ("solutions.01_02_embeddings", "Embeddings", True, "main"),
    ("solutions.01_03_entity_extraction", "Entity Extraction", True, "main"),
    ("solutions.02_01_vector_retriever", "Vector Retriever", False, "main"),
    ("solutions.02_02_vector_cypher_retriever", "Vector Cypher Retriever", False, "main"),
    ("solutions.02_03_text2cypher_retriever", "Text2Cypher Retriever", False, "main"),
    ("solutions.03_01_simple_agent", "Simple Agent", True, "run_agent"),
    ("solutions.03_02_vector_graph_agent", "Vector Graph Agent", True, "run_agent"),
    ("solutions.03_03_text2cypher_agent", "Text2Cypher Agent", True, "run_agent"),
    ("solutions.05_01_fulltext_search", "Fulltext Search", False, "main"),
    ("solutions.05_02_hybrid_search", "Hybrid Search", False, "main"),
]

# Default queries for agent solutions
AGENT_QUERIES = {
    "solutions.03_01_simple_agent": "Summarise the schema of the graph database.",
    "solutions.03_02_vector_graph_agent": "What risk factors are mentioned in Apple's financial documents?",
    "solutions.03_03_text2cypher_agent": "What stock has Microsoft issued?",
}


def print_menu():
    """Print the solution menu."""
    print("\n" + "=" * 50)
    print("Workshop Solutions")
    print("=" * 50)

    print("\nData Pipeline - WARNING! These will delete all data:")
    print("  1. Data Loading Fundamentals")
    print("  2. Embeddings")
    print("  3. Entity Extraction")

    print("\nRetrievers:")
    print("  4. Vector Retriever")
    print("  5. Vector Cypher Retriever")
    print("  6. Text2Cypher Retriever")

    print("\nAgents:")
    print("  7. Simple Agent")
    print("  8. Vector Graph Agent")
    print("  9. Text2Cypher Agent")

    print("\nSearch:")
    print(" 10. Fulltext Search")
    print(" 11. Hybrid Search")

    print("\n  A. Run all (from 02_01 onward)")
    print("  0. Exit")
    print("=" * 50)


def run_solution(choice: int) -> bool:
    """Run the selected solution. Returns False to exit."""
    if choice == 0:
        return False

    if choice < 1 or choice > len(SOLUTIONS):
        print("Invalid choice. Please try again.")
        return True

    module_name, title, is_async, entry_func = SOLUTIONS[choice - 1]

    print(f"\n>>> Running: {title}")
    print("-" * 50)

    try:
        module = importlib.import_module(module_name)
        func = getattr(module, entry_func)

        if is_async:
            if entry_func == "run_agent":
                query = AGENT_QUERIES.get(module_name, "Hello")
                asyncio.run(func(query))
            else:
                asyncio.run(func())
        else:
            func()

    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        raise
    except Exception as e:
        print(f"Error: {e}")

    print("-" * 50)
    return True


def run_all_from_02():
    """Run all solutions from 02_01 onward."""
    print("\n>>> Running all solutions from 02_01 onward...")
    # Solutions 4-11 correspond to indices 3-10 (02_01 onward)
    try:
        for i in range(4, len(SOLUTIONS) + 1):
            run_solution(i)
        print("\n>>> All solutions completed!")
    except KeyboardInterrupt:
        print("\n\nExiting.")
        sys.exit(0)


def main():
    """Main menu loop."""
    # Check for command-line argument
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.upper() == "A":
            run_all_from_02()
            return
        try:
            choice = int(arg)
            run_solution(choice)
            return
        except ValueError:
            print(f"Invalid argument: {arg}")
            print("Usage: uv run python main.py [1-11|A]")
            return

    print("Workshop Solution Runner")

    while True:
        print_menu()
        try:
            choice = input("\nSelect solution (0-11, A): ").strip()
            if not choice:
                continue
            if choice.upper() == "A":
                run_all_from_02()
                continue
            choice = int(choice)
        except ValueError:
            print("Please enter a number or 'A'.")
            continue
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        try:
            if not run_solution(choice):
                print("Goodbye!")
                break
        except KeyboardInterrupt:
            print("\n\nExiting.")
            break


if __name__ == "__main__":
    main()
