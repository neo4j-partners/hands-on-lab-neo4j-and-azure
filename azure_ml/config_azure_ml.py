"""
Azure ML Studio compatible configuration for GraphRAG workshops.

This module provides configuration that works with Azure ML's managed identity
authentication, eliminating the need for Azure CLI login.

Usage:
    Copy this file to your Azure ML notebook directory and import it instead
    of the standard config.py.
"""

from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from azure.identity import (
    ChainedTokenCredential,
    ManagedIdentityCredential,
    AzureCliCredential,
    DefaultAzureCredential,
)
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.llm import OpenAILLM
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env from current directory or parent
for env_path in [Path(".env"), Path("../.env"), Path("../../.env")]:
    if env_path.exists():
        load_dotenv(env_path)
        break


class Neo4jConfig(BaseSettings):
    """Neo4j configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    uri: str = Field(validation_alias="NEO4J_URI")
    username: str = Field(validation_alias="NEO4J_USERNAME")
    password: str = Field(validation_alias="NEO4J_PASSWORD")


class AgentConfig(BaseSettings):
    """Agent configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    project_endpoint: str = Field(validation_alias="AZURE_AI_PROJECT_ENDPOINT")
    model_name: str = Field(
        default="gpt-4o-mini", validation_alias="AZURE_AI_MODEL_NAME"
    )
    embedding_name: str = Field(
        default="text-embedding-ada-002",
        validation_alias="AZURE_AI_EMBEDDING_NAME",
    )
    # Optional: specify a user-assigned managed identity client ID
    managed_identity_client_id: Optional[str] = Field(
        default=None, validation_alias="AZURE_MANAGED_IDENTITY_CLIENT_ID"
    )

    @computed_field
    @property
    def inference_endpoint(self) -> str:
        """Get the model inference endpoint from project endpoint."""
        if "/api/projects/" in self.project_endpoint:
            base = self.project_endpoint.split("/api/projects/")[0]
            return f"{base}/models"
        return self.project_endpoint


@contextmanager
def get_neo4j_driver():
    """Context manager for Neo4j driver connection."""
    config = Neo4jConfig()
    driver = GraphDatabase.driver(
        config.uri,
        auth=(config.username, config.password),
    )
    try:
        yield driver
    finally:
        driver.close()


def get_agent_config() -> AgentConfig:
    """Get agent configuration from environment."""
    return AgentConfig()


def _get_azure_token() -> str:
    """
    Get Azure token for cognitive services.

    Authentication priority for Azure ML:
    1. User-assigned managed identity (if AZURE_MANAGED_IDENTITY_CLIENT_ID is set)
    2. System-assigned managed identity (default for Azure ML compute)
    3. Azure CLI credential (for local development/testing)
    4. Default Azure credential chain (fallback)

    Returns:
        str: Azure access token for Cognitive Services

    Raises:
        RuntimeError: If all authentication methods fail
    """
    scope = "https://cognitiveservices.azure.com/.default"
    config = get_agent_config()

    credentials = []

    # Priority 1: User-assigned managed identity (if configured)
    if config.managed_identity_client_id:
        credentials.append(
            ManagedIdentityCredential(client_id=config.managed_identity_client_id)
        )

    # Priority 2: System-assigned managed identity
    credentials.append(ManagedIdentityCredential())

    # Priority 3: Azure CLI (for local development)
    credentials.append(AzureCliCredential())

    # Try each credential in order
    errors = []
    for credential in credentials:
        try:
            token = credential.get_token(scope)
            return token.token
        except Exception as e:
            errors.append(f"{type(credential).__name__}: {e}")

    # Final fallback: DefaultAzureCredential
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token(scope)
        return token.token
    except Exception as e:
        errors.append(f"DefaultAzureCredential: {e}")

    raise RuntimeError(
        "Azure authentication failed. Tried:\n"
        + "\n".join(f"  - {err}" for err in errors)
        + "\n\nFor Azure ML, ensure the compute instance's managed identity "
        "has 'Cognitive Services User' role on your Azure AI resource."
    )


def get_embedder() -> OpenAIEmbeddings:
    """
    Get embedder using Microsoft Foundry's OpenAI-compatible endpoint.

    Uses managed identity authentication in Azure ML environments.
    """
    config = get_agent_config()
    token = _get_azure_token()

    return OpenAIEmbeddings(
        model=config.embedding_name,
        base_url=config.inference_endpoint,
        api_key=token,
    )


def get_llm() -> OpenAILLM:
    """
    Get LLM using Microsoft Foundry's OpenAI-compatible endpoint.

    Uses managed identity authentication in Azure ML environments.
    """
    config = get_agent_config()
    token = _get_azure_token()

    return OpenAILLM(
        model_name=config.model_name,
        base_url=config.inference_endpoint,
        api_key=token,
    )


# Convenience function to test authentication
def test_authentication() -> bool:
    """
    Test Azure authentication and print diagnostic information.

    Returns:
        bool: True if authentication succeeded, False otherwise
    """
    print("Testing Azure authentication...")
    try:
        token = _get_azure_token()
        print(f"  Authentication successful!")
        print(f"  Token preview: {token[:20]}...")
        return True
    except Exception as e:
        print(f"  Authentication failed: {e}")
        return False


def test_neo4j_connection() -> bool:
    """
    Test Neo4j connection and print diagnostic information.

    Returns:
        bool: True if connection succeeded, False otherwise
    """
    print("Testing Neo4j connection...")
    try:
        config = Neo4jConfig()
        print(f"  URI: {config.uri}")
        driver = GraphDatabase.driver(
            config.uri,
            auth=(config.username, config.password),
        )
        driver.verify_connectivity()
        driver.close()
        print("  Connection successful!")
        return True
    except Exception as e:
        print(f"  Connection failed: {e}")
        return False


if __name__ == "__main__":
    # Run diagnostic tests
    print("=" * 50)
    print("Azure ML Configuration Diagnostics")
    print("=" * 50)
    print()
    test_neo4j_connection()
    print()
    test_authentication()
    print()
    print("=" * 50)
