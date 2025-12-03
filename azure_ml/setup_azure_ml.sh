#!/bin/bash
# Azure ML Setup Script for GraphRAG Lab 5
#
# This script helps configure Azure ML resources for running the GraphRAG notebooks.
# Run this from your local machine before uploading notebooks to Azure ML.
#
# Usage: ./setup_azure_ml.sh [options]
#   -w, --workspace    Azure ML workspace name
#   -g, --resource-group   Resource group name
#   -c, --compute      Compute instance name (default: graphrag-compute)
#   -s, --sku          Compute SKU (default: Standard_DS3_v2)

set -e

# Default values
COMPUTE_NAME="graphrag-compute"
COMPUTE_SKU="Standard_DS3_v2"
WORKSPACE_NAME=""
RESOURCE_GROUP=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -w|--workspace)
            WORKSPACE_NAME="$2"
            shift 2
            ;;
        -g|--resource-group)
            RESOURCE_GROUP="$2"
            shift 2
            ;;
        -c|--compute)
            COMPUTE_NAME="$2"
            shift 2
            ;;
        -s|--sku)
            COMPUTE_SKU="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "  -w, --workspace      Azure ML workspace name"
            echo "  -g, --resource-group Resource group name"
            echo "  -c, --compute        Compute instance name (default: graphrag-compute)"
            echo "  -s, --sku            Compute SKU (default: Standard_DS3_v2)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$WORKSPACE_NAME" ] || [ -z "$RESOURCE_GROUP" ]; then
    echo "Error: Workspace name (-w) and resource group (-g) are required"
    exit 1
fi

echo "========================================"
echo "Azure ML Setup for GraphRAG Lab 5"
echo "========================================"
echo ""
echo "Configuration:"
echo "  Workspace:      $WORKSPACE_NAME"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Compute Name:   $COMPUTE_NAME"
echo "  Compute SKU:    $COMPUTE_SKU"
echo ""

# Check if logged in to Azure
echo "Checking Azure CLI login status..."
if ! az account show &>/dev/null; then
    echo "Not logged in. Running az login..."
    az login --use-device-code
fi

SUBSCRIPTION=$(az account show --query id -o tsv)
echo "Using subscription: $SUBSCRIPTION"
echo ""

# Check if ML extension is installed
echo "Checking Azure ML extension..."
if ! az extension show --name ml &>/dev/null; then
    echo "Installing Azure ML extension..."
    az extension add --name ml --yes
fi

# Check if workspace exists
echo "Checking if workspace exists..."
if ! az ml workspace show --name "$WORKSPACE_NAME" --resource-group "$RESOURCE_GROUP" &>/dev/null; then
    echo "Workspace not found. Creating workspace..."
    az ml workspace create \
        --name "$WORKSPACE_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --location "$(az group show --name "$RESOURCE_GROUP" --query location -o tsv)"
else
    echo "Workspace exists."
fi

# Check if compute instance exists
echo "Checking compute instance..."
if ! az ml compute show --name "$COMPUTE_NAME" --workspace-name "$WORKSPACE_NAME" --resource-group "$RESOURCE_GROUP" &>/dev/null; then
    echo "Creating compute instance..."
    az ml compute create \
        --name "$COMPUTE_NAME" \
        --workspace-name "$WORKSPACE_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --type ComputeInstance \
        --size "$COMPUTE_SKU"
    echo "Compute instance created. Waiting for it to start..."
    sleep 30
else
    echo "Compute instance exists."
fi

# Get compute identity
echo ""
echo "Getting compute instance identity..."
COMPUTE_IDENTITY=$(az ml compute show \
    --name "$COMPUTE_NAME" \
    --workspace-name "$WORKSPACE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query identity.principal_id -o tsv 2>/dev/null || echo "")

if [ -n "$COMPUTE_IDENTITY" ]; then
    echo "Compute identity: $COMPUTE_IDENTITY"
else
    echo "Note: Compute instance identity not found. You may need to:"
    echo "  1. Wait for compute to finish provisioning"
    echo "  2. Enable system-assigned managed identity manually"
fi

# Get AI Services resource
echo ""
echo "Looking for Azure AI Services in resource group..."
AI_SERVICES=$(az cognitiveservices account list --resource-group "$RESOURCE_GROUP" --query "[0].name" -o tsv 2>/dev/null || echo "")

if [ -n "$AI_SERVICES" ] && [ -n "$COMPUTE_IDENTITY" ]; then
    echo "Found AI Services: $AI_SERVICES"
    echo "Assigning Cognitive Services User role to compute instance..."

    AI_SERVICES_ID=$(az cognitiveservices account show \
        --name "$AI_SERVICES" \
        --resource-group "$RESOURCE_GROUP" \
        --query id -o tsv)

    # Check if role already assigned
    EXISTING_ROLE=$(az role assignment list \
        --assignee "$COMPUTE_IDENTITY" \
        --scope "$AI_SERVICES_ID" \
        --role "Cognitive Services User" \
        --query "[0].id" -o tsv 2>/dev/null || echo "")

    if [ -z "$EXISTING_ROLE" ]; then
        az role assignment create \
            --assignee "$COMPUTE_IDENTITY" \
            --role "Cognitive Services User" \
            --scope "$AI_SERVICES_ID"
        echo "Role assigned successfully."
    else
        echo "Role already assigned."
    fi
else
    if [ -z "$AI_SERVICES" ]; then
        echo "Warning: No Azure AI Services found in resource group."
        echo "Ensure you've run 'azd up' to deploy the infrastructure."
    fi
fi

# Export environment values
echo ""
echo "========================================"
echo "Environment Configuration"
echo "========================================"
echo ""
echo "Add these to your .env file in Azure ML:"
echo ""

# Get environment values from azd if available
if command -v azd &>/dev/null; then
    AZD_ENV=$(azd env get-values 2>/dev/null || echo "")
    if [ -n "$AZD_ENV" ]; then
        echo "$AZD_ENV" | grep -E "^(NEO4J_|AZURE_AI_)" || true
    fi
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Go to https://ml.azure.com"
echo "  2. Select workspace: $WORKSPACE_NAME"
echo "  3. Upload notebooks from Lab_5_GraphRAG_Retrievers/"
echo "  4. Upload config_azure_ml.py from azure_ml/"
echo "  5. Create .env file with your credentials"
echo "  6. Run the notebooks using compute: $COMPUTE_NAME"
