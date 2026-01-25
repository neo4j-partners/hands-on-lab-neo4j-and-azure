"""Utilities for data loading and Neo4j operations."""

import sys
from pathlib import Path
from neo4j import GraphDatabase

sys.path.insert(0, '../new-workshops/solutions')
from config import Neo4jConfig


class Neo4jConnection:
    """Manages Neo4j database connection."""

    def __init__(self):
        """Initialize and connect to Neo4j using environment configuration."""
        self.config = Neo4jConfig()
        self.driver = GraphDatabase.driver(
            self.config.uri,
            auth=(self.config.username, self.config.password)
        )

    def verify(self):
        """Verify the connection is working."""
        self.driver.verify_connectivity()
        print("Connected to Neo4j successfully!")
        return self

    def clear_graph(self):
        """Remove all Document and Chunk nodes."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n) WHERE n:Document OR n:Chunk
                DETACH DELETE n
                RETURN count(n) as deleted
            """)
            count = result.single()["deleted"]
            print(f"Deleted {count} nodes")
        return self

    def close(self):
        """Close the database connection."""
        self.driver.close()
        print("Connection closed.")


class DataLoader:
    """Handles loading text data from files."""

    def __init__(self, file_path: str):
        """Initialize with path to data file.

        Args:
            file_path: Path to the text file to load.
        """
        self.file_path = Path(file_path)
        self._text = None

    @property
    def text(self) -> str:
        """Load and return the text content from the file."""
        if self._text is None:
            self._text = self.file_path.read_text().strip()
        return self._text

    def get_metadata(self) -> dict:
        """Return metadata about the loaded file."""
        return {
            "path": str(self.file_path),
            "name": self.file_path.name,
            "size": len(self.text)
        }

    def split_into_chunks(self, separator: str = "\n\n") -> list[str]:
        """Split text into chunks by the given separator.

        Args:
            separator: String to split on. Defaults to double newlines (paragraphs).

        Returns:
            List of non-empty chunks.
        """
        chunks = [chunk.strip() for chunk in self.text.split(separator) if chunk.strip()]
        return chunks
