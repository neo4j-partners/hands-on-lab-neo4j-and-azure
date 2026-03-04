#!/bin/bash
# Codespace start script - creates CONFIG.txt and displays setup instructions

# Create CONFIG.txt with Neo4j secrets if they exist (only if CONFIG.txt doesn't already exist)
if [ ! -f CONFIG.txt ]; then
    if [ -n "$NEO4J_URI" ] || [ -n "$NEO4J_USERNAME" ] || [ -n "$NEO4J_PASSWORD" ]; then
        echo "Creating CONFIG.txt with Neo4j configuration..."
        cat > CONFIG.txt << EOF
# Neo4j Connection (from Codespace secrets)
NEO4J_URI=${NEO4J_URI:-}
NEO4J_USERNAME=${NEO4J_USERNAME:-}
NEO4J_PASSWORD=${NEO4J_PASSWORD:-}
NEO4J_VECTOR_INDEX_NAME=chunkEmbeddings
NEO4J_FULLTEXT_INDEX_NAME=search_chunks
NEO4J_FULLTEXT_ENTITY_INDEX_NAME=search_entities

# Embedding Configuration
EMBEDDING_DIMENSIONS=1536

# Azure Configuration — get your project endpoint from the Foundry portal (ai.azure.com)
AZURE_AI_PROJECT_ENDPOINT=
AZURE_AI_MODEL_NAME=gpt-4o-mini
AZURE_AI_EMBEDDING_NAME=text-embedding-3-small
EOF
        echo "✅ CONFIG.txt created with Neo4j configuration"
    else
        echo "⚠️  No Neo4j secrets found - CONFIG.txt not created"
        echo "   Set secrets in Codespace settings or create CONFIG.txt manually"
    fi
else
    echo "✅ CONFIG.txt already exists - preserving existing configuration"
fi

echo ""
echo "✅ Ready! Run:"
echo "   az login --use-device-code"
echo ""
echo "Then edit CONFIG.txt and add your Azure Foundry project endpoint from Lab 3:"
echo "   AZURE_AI_PROJECT_ENDPOINT=https://<resource-name>.services.ai.azure.com/api/projects/<project-name>"
echo "   AZURE_AI_MODEL_NAME=gpt-4o-mini"
echo "   AZURE_AI_EMBEDDING_NAME=text-embedding-3-small"
echo ""
echo "To populate the Neo4j database with sample data, run:"
echo "   uv run scripts/restore_neo4j.py"
echo ""
