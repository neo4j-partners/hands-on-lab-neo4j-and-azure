# Infrastructure Proposal: Azure ML Integration

This document proposes how to extend the existing `infra/` Bicep templates to optionally deploy Azure Machine Learning resources for running the GraphRAG workshops.

## Overview

The current infrastructure deploys:
- Azure AI Services (OpenAI models)
- Azure AI Project (Microsoft Foundry)
- Storage Account
- Application Insights & Log Analytics
- Optional: Container Apps for API deployment

This proposal adds an **optional** Azure ML workspace with compute resources, enabling workshop participants to run notebooks in a managed Azure environment.

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Resource Group                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │  Azure AI        │    │  Azure ML        │                   │
│  │  Services        │◄───│  Workspace       │                   │
│  │  (OpenAI)        │    │                  │                   │
│  └──────────────────┘    └────────┬─────────┘                   │
│                                   │                              │
│  ┌──────────────────┐    ┌────────▼─────────┐                   │
│  │  Storage         │◄───│  Compute         │                   │
│  │  Account         │    │  Instance        │                   │
│  └──────────────────┘    └──────────────────┘                   │
│                                                                  │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │  Key Vault       │    │  Container       │                   │
│  │  (ML secrets)    │    │  Registry        │                   │
│  └──────────────────┘    └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                          ┌──────────────────┐
                          │  Neo4j Aura      │
                          │  (External)      │
                          └──────────────────┘
```

## Implementation Plan

### 1. New Parameter in `main.bicep`

Add a toggle parameter to enable Azure ML deployment:

```bicep
@description('Deploy Azure ML workspace for notebook execution')
param deployAzureML bool = false

@description('Azure ML compute instance SKU')
param azureMLComputeSku string = 'Standard_DS3_v2'

@description('Auto-shutdown time for compute (HH:MM, empty to disable)')
param azureMLAutoShutdownTime string = '19:00'
```

### 2. New Bicep Module: `infra/core/host/ml-workspace.bicep`

```bicep
@description('Name of the Azure ML workspace')
param workspaceName string

@description('Location for all resources')
param location string = resourceGroup().location

@description('Storage account ID for workspace')
param storageAccountId string

@description('Application Insights ID for workspace')
param applicationInsightsId string

@description('Tags to apply to resources')
param tags object = {}

@description('Compute instance name')
param computeInstanceName string = 'graphrag-compute'

@description('Compute instance SKU')
param computeInstanceSku string = 'Standard_DS3_v2'

@description('Auto-shutdown time (HH:MM in UTC, empty to disable)')
param autoShutdownTime string = ''

// Key Vault for ML workspace secrets
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  properties: {
    tenantId: tenant().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
  }
}

// Container Registry for ML workspace
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'cr${uniqueString(resourceGroup().id)}'
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
  }
}

// Azure ML Workspace
resource mlWorkspace 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: workspaceName
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: workspaceName
    storageAccount: storageAccountId
    keyVault: keyVault.id
    applicationInsights: applicationInsightsId
    containerRegistry: containerRegistry.id
    publicNetworkAccess: 'Enabled'
  }
}

// Compute Instance
resource computeInstance 'Microsoft.MachineLearningServices/workspaces/computes@2024-04-01' = {
  parent: mlWorkspace
  name: computeInstanceName
  location: location
  tags: tags
  properties: {
    computeType: 'ComputeInstance'
    properties: {
      vmSize: computeInstanceSku
      applicationSharingPolicy: 'Personal'
      sshSettings: {
        sshPublicAccess: 'Disabled'
      }
      schedules: !empty(autoShutdownTime) ? {
        computeStartStop: [
          {
            action: 'Stop'
            triggerType: 'Cron'
            cron: {
              expression: '0 ${split(autoShutdownTime, ':')[1]} ${split(autoShutdownTime, ':')[0]} * * *'
              startTime: '2024-01-01T00:00:00Z'
              timezone: 'UTC'
            }
            status: 'Enabled'
          }
        ]
      } : null
    }
  }
}

output workspaceId string = mlWorkspace.id
output workspaceName string = mlWorkspace.name
output computeInstanceName string = computeInstance.name
output workspacePrincipalId string = mlWorkspace.identity.principalId
output computeInstancePrincipalId string = computeInstance.identity.principalId
```

### 3. Update `main.bicep` to Include ML Module

```bicep
// Azure ML workspace (optional)
module mlWorkspace 'core/host/ml-workspace.bicep' = if (deployAzureML) {
  name: 'ml-workspace'
  params: {
    workspaceName: 'ml-${resourceToken}'
    location: location
    tags: tags
    storageAccountId: ai.outputs.storageAccountId
    applicationInsightsId: ai.outputs.applicationInsightsId
    computeInstanceName: 'graphrag-${resourceToken}'
    computeInstanceSku: azureMLComputeSku
    autoShutdownTime: azureMLAutoShutdownTime
  }
}

// Role assignment for ML workspace to access AI Services
module mlWorkspaceAIAccess 'core/security/role.bicep' = if (deployAzureML && !skipRoleAssignments) {
  name: 'ml-workspace-ai-access'
  params: {
    principalType: 'ServicePrincipal'
    principalId: mlWorkspace.outputs.workspacePrincipalId
    roleDefinitionId: 'a97b65f3-24c7-4388-baec-2e87135dc908' // Cognitive Services User
  }
}

// Role assignment for ML compute instance to access AI Services
module mlComputeAIAccess 'core/security/role.bicep' = if (deployAzureML && !skipRoleAssignments) {
  name: 'ml-compute-ai-access'
  params: {
    principalType: 'ServicePrincipal'
    principalId: mlWorkspace.outputs.computeInstancePrincipalId
    roleDefinitionId: 'a97b65f3-24c7-4388-baec-2e87135dc908' // Cognitive Services User
  }
}
```

### 4. Add Outputs for Azure ML

```bicep
// Azure ML outputs (empty when deployAzureML=false)
output AZURE_ML_WORKSPACE_NAME string = deployAzureML ? mlWorkspace.outputs.workspaceName : ''
output AZURE_ML_COMPUTE_INSTANCE string = deployAzureML ? mlWorkspace.outputs.computeInstanceName : ''
output AZURE_ML_WORKSPACE_URL string = deployAzureML ? 'https://ml.azure.com/home?wsid=${mlWorkspace.outputs.workspaceId}' : ''
```

### 5. Update `main.parameters.json`

Add default values:

```json
{
  "deployAzureML": {
    "value": false
  },
  "azureMLComputeSku": {
    "value": "Standard_DS3_v2"
  },
  "azureMLAutoShutdownTime": {
    "value": "19:00"
  }
}
```

## Usage

### Deploy with Azure ML Enabled

```bash
# Using azd
azd up --parameters deployAzureML=true

# Or update azure.yaml to set the parameter
```

### Deploy without Azure ML (default)

```bash
azd up
```

## Required Bicep Modules

### `infra/core/host/ml-workspace.bicep` (New)

Full implementation provided above.

### Updates to Existing Modules

#### `infra/core/host/ai-environment.bicep`

Add output for storage account ID:

```bicep
output storageAccountId string = storageAccount.id
output applicationInsightsId string = applicationInsights.id
```

## Role Assignments

The ML workspace and compute instance need:

| Principal | Role | Scope | Purpose |
|-----------|------|-------|---------|
| ML Workspace | Cognitive Services User | AI Services | Access OpenAI models |
| Compute Instance | Cognitive Services User | AI Services | Run notebooks with AI |
| Compute Instance | Storage Blob Data Contributor | Storage Account | Read/write notebooks |

## Cost Considerations

| Resource | SKU | Est. Monthly Cost |
|----------|-----|------------------|
| ML Workspace | N/A (free) | $0 |
| Compute Instance | Standard_DS3_v2 | ~$150-200 (if running 24/7) |
| Container Registry | Basic | ~$5 |
| Key Vault | Standard | ~$0.03/operation |

**Recommendations:**
- Auto-shutdown is enabled by default (19:00 UTC)
- Stop compute when not in use
- Consider smaller SKU for basic notebooks

## Alternative Approaches Considered

### 1. Azure ML Serverless Compute
- **Pros**: No always-on compute costs
- **Cons**: Cold start latency, less predictable pricing

### 2. Azure Notebooks (deprecated)
- Not recommended as service is being retired

### 3. GitHub Codespaces Integration
- Already supported via existing `.devcontainer/`
- Azure ML adds enterprise features (RBAC, private endpoints)

## Security Considerations

1. **Network Isolation**: For production, consider:
   - Private endpoints for ML workspace
   - VNet integration for compute

2. **Secrets Management**:
   - Neo4j credentials should be stored in Key Vault
   - Use managed identity, not connection strings

3. **Access Control**:
   - RBAC on ML workspace
   - Compute instance is personal by default

## Migration Path

For existing deployments:

1. Run `azd up --parameters deployAzureML=true`
2. Azure will add ML resources without affecting existing resources
3. Configure compute instance with `.env` file
4. Upload notebooks to ML workspace

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `infra/main.bicep` | Modify | Add ML parameters and module reference |
| `infra/main.parameters.json` | Modify | Add default parameter values |
| `infra/core/host/ml-workspace.bicep` | Create | New ML workspace module |
| `infra/core/host/ai-environment.bicep` | Modify | Add storage/appinsights ID outputs |

## Implementation Checklist

- [ ] Create `infra/core/host/ml-workspace.bicep`
- [ ] Update `infra/core/host/ai-environment.bicep` with new outputs
- [ ] Update `infra/main.bicep` with ML parameters and module
- [ ] Update `infra/main.parameters.json` with defaults
- [ ] Test deployment with `deployAzureML=true`
- [ ] Test deployment with `deployAzureML=false` (backward compatibility)
- [ ] Verify role assignments work correctly
- [ ] Document in main README

## Appendix: Complete ml-workspace.bicep

See the full module code in section 2 above, ready to be copied to `infra/core/host/ml-workspace.bicep`.
