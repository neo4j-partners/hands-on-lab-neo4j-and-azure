metadata description = 'Creates a role assignment for a service principal. Skips if principalId is empty.'
param principalId string

@allowed([
  'Device'
  'ForeignGroup'
  'Group'
  'ServicePrincipal'
  'User'
  ''
])
param principalType string = ''
param roleDefinitionId string

// Only create if principalId is provided (makes redeployments safer)
resource role 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(subscription().id, resourceGroup().id, principalId, roleDefinitionId)
  properties: {
    principalId: principalId
    // Only set principalType if provided - avoids conflicts on redeployment
    principalType: !empty(principalType) ? principalType : null
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
  }
}
