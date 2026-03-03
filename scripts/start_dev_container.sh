#!/bin/bash
# Codespace start script - creates .env and displays setup instructions

# Create .env with Neo4j secrets if they exist (only if .env doesn't already exist)
if [ ! -f .env ]; then
    if [ -n "$NEO4J_URI" ] || [ -n "$NEO4J_USERNAME" ] || [ -n "$NEO4J_PASSWORD" ]; then
        echo "Creating .env with Neo4j configuration..."
        cat > .env << EOF
# Neo4j Connection (from Codespace secrets)
NEO4J_URI=${NEO4J_URI:-}
NEO4J_USERNAME=${NEO4J_USERNAME:-}
NEO4J_PASSWORD=${NEO4J_PASSWORD:-}
NEO4J_VECTOR_INDEX_NAME=chunkEmbeddings
NEO4J_FULLTEXT_INDEX_NAME=search_chunks
NEO4J_FULLTEXT_ENTITY_INDEX_NAME=search_entities

# Embedding Configuration
EMBEDDING_DIMENSIONS=1536
EOF
        echo "✅ .env created with Neo4j configuration"
    else
        echo "⚠️  No Neo4j secrets found - .env not created"
        echo "   Set secrets in Codespace settings or create .env manually"
    fi
else
    echo "✅ .env already exists - preserving existing configuration"
fi

echo ""
echo "✅ Ready! Run:"
echo "   az login --use-device-code"
echo ""
echo "Then edit .env and add your Azure Foundry project endpoint from Lab 3:"
echo "   AZURE_AI_PROJECT_ENDPOINT=https://<resource-name>.services.ai.azure.com/api/projects/<project-name>"
echo "   AZURE_AI_MODEL_NAME=gpt-4o-mini"
echo "   AZURE_AI_EMBEDDING_NAME=text-embedding-3-small"
echo ""
echo "To populate the Neo4j database with sample data, run:"
echo "   uv run scripts/restore_neo4j.py"
echo ""
