#!/bin/bash
# Configure Azure region for Financial Data Load Workshop
# Run this after: az login --use-device-code && azd auth login --use-device-code

set -e

ENV_FILE=".env"

# Function to clean stale Azure config from .env
clean_env_file() {
    if [ ! -f "$ENV_FILE" ]; then
        return
    fi

    if grep -qE '^(AZURE_|SERVICE_)' "$ENV_FILE" 2>/dev/null; then
        echo ""
        echo "Found existing Azure configuration in .env."

        if grep -qE '^NEO4J_' "$ENV_FILE" 2>/dev/null; then
            grep '^NEO4J_' "$ENV_FILE" > "$ENV_FILE.neo4j.tmp"

            cat > "$ENV_FILE" << 'EOF'
# Neo4j Connection (preserved)

EOF
            cat "$ENV_FILE.neo4j.tmp" >> "$ENV_FILE"
            rm -f "$ENV_FILE.neo4j.tmp"

            echo "Removed stale Azure config (Neo4j settings preserved)"
        else
            grep -vE '^(AZURE_|SERVICE_)' "$ENV_FILE" > "$ENV_FILE.tmp" || true
            mv "$ENV_FILE.tmp" "$ENV_FILE"
            echo "Cleaned stale Azure configuration"
        fi
    fi
}

# Function to check if Azure resources are deployed
check_deployed_resources() {
    if [ ! -d ".azure" ] || [ ! -f ".azure/dev/.env" ]; then
        return 1  # No state, nothing deployed
    fi

    # Source the azd environment to get resource group
    local rg=$(grep '^AZURE_RESOURCE_GROUP=' ".azure/dev/.env" 2>/dev/null | cut -d'=' -f2 | tr -d '"')

    if [ -z "$rg" ]; then
        return 1  # No resource group in state
    fi

    # Check if resource group exists in Azure
    if az group show --name "$rg" >/dev/null 2>&1; then
        echo "$rg"
        return 0  # Resources are deployed
    fi

    return 1  # Resource group doesn't exist
}

echo ""
echo "Azure AI Foundry serverless models require one of these regions:"
echo "  1) East US 2 (eastus2) - Recommended"
echo "  2) Sweden Central (swedencentral)"
echo "  3) West US 2 (westus2)"
echo "  4) West US 3 (westus3)"
echo ""
read -p "Select a region [1-4] (default: 1): " choice
choice=${choice:-1}

case $choice in
    1) REGION="eastus2" ;;
    2) REGION="swedencentral" ;;
    3) REGION="westus2" ;;
    4) REGION="westus3" ;;
    *)
        echo "Invalid choice. Please enter 1-4."
        exit 1
        ;;
esac

clean_env_file

if [ -d ".azure" ]; then
    deployed_rg=$(check_deployed_resources)
    if [ $? -eq 0 ]; then
        echo ""
        echo "WARNING: Found deployed Azure resources in resource group '$deployed_rg'"
        echo "Deleting .azure directory will orphan these resources."
        echo ""
        echo "Options:"
        echo "  1) Run 'azd down' first to clean up deployed resources"
        echo "  2) Continue anyway (resources will be orphaned)"
        echo ""
        read -p "Continue without cleanup? [y/N]: " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo "Aborted. Run 'azd down' first, then re-run this script."
            exit 0
        fi
        echo "Proceeding with .azure directory removal..."
    fi
    echo "Removing existing .azure directory..."
    rm -rf .azure
fi

echo "Initializing azd environment..."
azd init -e dev

azd env set AZURE_LOCATION "$REGION"

echo ""
echo "Azure configured: $REGION"
echo ""
echo "Ready to deploy! Run:"
echo "   azd up"
echo "   uv run python setup_env.py"
