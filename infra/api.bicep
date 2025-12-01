param name string
param location string = resourceGroup().location
param tags object = {}

param containerRegistryName string
param identityName string
param containerAppsEnvironmentName string
param azureAIProjectEndpoint string
param azureOpenAIEndpoint string
param azureModelDeploymentName string
param agentName string
param enableAzureMonitorTracing bool = true

@description('Skip role assignment for ACR pull (use on redeployment)')
param skipRoleAssignment bool = false

resource apiIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

var env = [
  {
    name: 'AZURE_CLIENT_ID'
    value: apiIdentity.properties.clientId
  }
  {
    name: 'AZURE_AI_PROJECT_ENDPOINT'
    value: azureAIProjectEndpoint
  }
  {
    name: 'AZURE_AI_MODEL_NAME'
    value: azureModelDeploymentName
  }
  {
    name: 'AZURE_AI_AGENT_NAME'
    value: agentName
  }
  {
    name: 'AZURE_OPENAI_ENDPOINT'
    value: azureOpenAIEndpoint
  }
  {
    name: 'RUNNING_IN_PRODUCTION'
    value: 'true'
  }
  {
    name: 'ENABLE_AZURE_MONITOR_TRACING'
    value: enableAzureMonitorTracing ? 'true' : 'false'
  }
]

module app 'core/host/container-app-upsert.bicep' = {
  name: 'container-app-module'
  params: {
    name: name
    location: location
    tags: union(tags, { 'azd-service-name': 'api' })
    identityName: apiIdentity.name
    containerRegistryName: containerRegistryName
    containerAppsEnvironmentName: containerAppsEnvironmentName
    targetPort: 50505
    env: env
    skipRoleAssignment: skipRoleAssignment
  }
}

output SERVICE_API_IDENTITY_PRINCIPAL_ID string = apiIdentity.properties.principalId
output SERVICE_API_NAME string = app.outputs.name
output SERVICE_API_URI string = app.outputs.uri
