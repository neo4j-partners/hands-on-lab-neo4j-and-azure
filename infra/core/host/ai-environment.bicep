@minLength(1)
@description('Primary location for all resources')
param location string

@description('The AI Project resource name.')
param aiProjectName string
@description('The Storage Account resource name.')
param storageAccountName string
@description('The Microsoft Foundry Services resource name.')
param aiServicesName string
@description('The Microsoft Foundry Services model deployments.')
param aiServiceModelDeployments array = []
@description('The Log Analytics resource name.')
param logAnalyticsName string = ''
@description('The Application Insights resource name.')
param applicationInsightsName string = ''
@description('The Azure Search resource name.')
param searchServiceName string = ''
@description('The Application Insights connection name.')
param appInsightConnectionName string
param tags object = {}
param aoaiConnectionName string
@description('Skip role assignments on redeployment')
param skipRoleAssignments bool = false
module storageAccount '../storage/storage-account.bicep' = {
  name: 'storageAccount'
  params: {
    location: location
    tags: tags
    name: storageAccountName
    containers: [
      {
        name: 'default'
      }
    ]
    files: [
      {
        name: 'default'
      }
    ]
    queues: [
      {
        name: 'default'
      }
    ]
    tables: [
      {
        name: 'default'
      }
    ]
    deleteRetentionPolicy: {
      allowPermanentDelete: false
      enabled: false
    }
    shareDeleteRetentionPolicy: {
      enabled: true
      days: 7
    }
  }
}

module logAnalytics '../monitor/loganalytics.bicep' =
  if (!empty(logAnalyticsName)) {
    name: 'logAnalytics'
    params: {
      location: location
      tags: tags
      name: logAnalyticsName
    }
  }

module applicationInsights '../monitor/applicationinsights.bicep' =
  if (!empty(applicationInsightsName) && !empty(logAnalyticsName)) {
    name: 'applicationInsights'
    params: {
      location: location
      tags: tags
      name: applicationInsightsName
      logAnalyticsWorkspaceId: !empty(logAnalyticsName) ? logAnalytics.outputs.id : ''
    }
  }

module cognitiveServices '../ai/cognitiveservices.bicep' = {
  name: 'cognitiveServices'
  params: {
    location: location
    tags: tags
    aiServiceName: aiServicesName
    aiProjectName: aiProjectName
    deployments: aiServiceModelDeployments
    appInsightsId: !empty(applicationInsightsName) && !empty(logAnalyticsName) ? applicationInsights.outputs.id : ''
    appInsightConnectionName: appInsightConnectionName
    appInsightConnectionString: !empty(applicationInsightsName) && !empty(logAnalyticsName) ? applicationInsights.outputs.connectionString : ''
    storageAccountId: storageAccount.outputs.id
    storageAccountConnectionName: storageAccount.outputs.name
    storageAccountBlobEndpoint: storageAccount.outputs.primaryEndpoints.blob
    aoaiConnectionName: aoaiConnectionName
  }
}

module accountStorageRoleAssignment '../../core/security/role.bicep' = if (!skipRoleAssignments) {
  name: 'ai-account-role-storage-contributor'
  params: {
    principalType: 'ServicePrincipal'
    principalId: cognitiveServices.outputs.accountPrincipalId
    roleDefinitionId: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe' // Storage Blob Data Contributor
  }
}

module projectStorageRoleAssignment '../../core/security/role.bicep' = if (!skipRoleAssignments) {
  name: 'ai-project-role-storage-contributor'
  params: {
    principalType: 'ServicePrincipal'
    principalId: cognitiveServices.outputs.projectPrincipalId
    roleDefinitionId: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe' // Storage Blob Data Contributor
  }
}

module projectAIUserRoleAssignment '../../core/security/role.bicep' = if (!skipRoleAssignments) {
  name: 'ai-project-role-ai-user'
  params: {
    principalType: 'ServicePrincipal'
    principalId: cognitiveServices.outputs.projectPrincipalId
    roleDefinitionId: '53ca6127-db72-4b80-b1b0-d745d6d5456d' // Microsoft Foundry User
  }
}

// REMOVED: searchService module


// Outputs
output storageAccountId string = storageAccount.outputs.id
output storageAccountName string = storageAccount.outputs.name

output applicationInsightsId string = !empty(applicationInsightsName) && !empty(logAnalyticsName) ? applicationInsights.outputs.id : ''
output applicationInsightsName string = !empty(applicationInsightsName) && !empty(logAnalyticsName) ? applicationInsights.outputs.name : ''
output applicationInsightsConnectionString string = !empty(applicationInsightsName) && !empty(logAnalyticsName) ? applicationInsights.outputs.connectionString : ''
output logAnalyticsWorkspaceId string = !empty(logAnalyticsName) ? logAnalytics.outputs.id : ''
output logAnalyticsWorkspaceName string = !empty(logAnalyticsName) ? logAnalytics.outputs.name : ''

output aiServiceId string = cognitiveServices.outputs.id
output aiServicesName string = cognitiveServices.outputs.name
output aiProjectEndpoint string = cognitiveServices.outputs.projectEndpoint
output openAIEndpoint string = cognitiveServices.outputs.openAIEndpoint
output aiServicePrincipalId string = cognitiveServices.outputs.accountPrincipalId

// REMOVED: searchService Outputs
output searchServiceId string = ''
output searchServiceName string = ''
output searchServiceEndpoint string = ''

output projectResourceId string = cognitiveServices.outputs.projectResourceId
output searchConnectionId string = ''