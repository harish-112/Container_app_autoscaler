param principalId string
param acrName string

var acrPullRoleDefinitionId = '7f951dda-4ed3-4680-a7ca-43fe172d538d' // AcrPull

resource targetAcr 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = {
  name: acrName
}

resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(principalId, targetAcr.id, acrPullRoleDefinitionId)
  scope: targetAcr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRoleDefinitionId)
    principalId: principalId
    principalType: 'ServicePrincipal'
  }
}
