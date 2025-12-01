#!/bin/bash
# Codespace start script - creates .env and displays setup instructions

# Create .env with Neo4j secrets if they exist
if [ -n "$NEO4J_URI" ] || [ -n "$NEO4J_USERNAME" ] || [ -n "$NEO4J_PASSWORD" ]; then
    echo "Creating .env with Neo4j configuration..."
    cat > .env << EOF
# Neo4j Connection (from Codespace secrets)
NEO4J_URI=${NEO4J_URI:-}
NEO4J_USERNAME=${NEO4J_USERNAME:-}
NEO4J_PASSWORD=${NEO4J_PASSWORD:-}
NEO4J_VECTOR_INDEX_NAME=chunkEmbeddings

# Embedding Configuration
EMBEDDING_DIMENSIONS=1536
EOF
    echo "✅ .env created with Neo4j configuration"
else
    echo "⚠️  No Neo4j secrets found - .env not created"
    echo "   Set secrets in Codespace settings or create .env manually"
fi

echo ""
echo "✅ Ready! Run:"
echo "   az login --use-device-code"
echo "   azd auth login --use-device-code"
echo "   ./scripts/setup_azure.sh"
echo "   azd up"
echo ""
echo "To populate the Neo4j database with sample data, run:"
echo "   uv run scripts/restore_neo4j.py"
echo ""
