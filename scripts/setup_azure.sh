#!/bin/bash
# Configure Azure region for workshop
# Run this after: az login --use-device-code && azd auth login --use-device-code

set -e

ENV_FILE=".env"

# Function to clean stale Azure config from .env
clean_env_file() {
    if [ ! -f "$ENV_FILE" ]; then
        return
    fi

    # Check if there are Azure/Service settings to clean
    if grep -qE '^(AZURE_|SERVICE_|EMBEDDING_)' "$ENV_FILE" 2>/dev/null; then
        echo ""
        echo "Found existing Azure configuration in .env that may conflict with new deployment."

        # Check for Neo4j settings and preserve them
        if grep -qE '^NEO4J_' "$ENV_FILE" 2>/dev/null; then
            # Extract Neo4j settings
            grep '^NEO4J_' "$ENV_FILE" > "$ENV_FILE.neo4j.tmp"

            # Rebuild .env with only Neo4j settings
            cat > "$ENV_FILE" << 'EOF'
# ============================================
# User Configuration
# ============================================
# Neo4j Connection (configure these manually)

EOF
            cat "$ENV_FILE.neo4j.tmp" >> "$ENV_FILE"
            rm -f "$ENV_FILE.neo4j.tmp"

            echo "Removed stale Azure config from .env (Neo4j settings preserved)"
        else
            # No Neo4j settings, safe to clean Azure config
            echo "Cleaning stale Azure configuration from .env..."
            grep -vE '^(AZURE_|SERVICE_|EMBEDDING_)' "$ENV_FILE" > "$ENV_FILE.tmp" || true
            mv "$ENV_FILE.tmp" "$ENV_FILE"
            echo "Done"
        fi
    fi
}

REGION="eastus2"
echo ""
echo "Using Azure region: $REGION"

# Clean stale Azure config from .env before azd init
clean_env_file

# Remove existing azd environment to start fresh
if [ -d ".azure" ]; then
    echo "Removing existing .azure directory..."
    rm -rf .azure
fi

# Initialize new azd environment
echo "Initializing azd environment..."
azd init -e workshop

azd env set AZURE_LOCATION "$REGION"

echo ""
echo "Azure configured: $REGION"
echo ""
echo "Ready to deploy! Run:"
echo "   azd up"
