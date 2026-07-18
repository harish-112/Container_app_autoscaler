param containerAppName string
param environmentId string
param imageName string
param cpu string = '0.5'
param memory string = '1.0Gi'

param minReplicas int
param maxReplicas int

param acrServer string
param acrResourceId string


var acrName = last(split(acrResourceId, '/'))
var acrResourceGroup = split(acrResourceId, '/')[4] // extracted 'construction-rg' name from the long resourceId string

// 1. Created the User-Assigned Identity
resource userIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${containerAppName}-identity'
  location: resourceGroup().location
}

// 2. Since ACR is from a different Resource Group, i need to perform cross resource configurationassign permissions by calling the module in the OTHER Resource Group
module assignAcrPull './acr-role-assignment.bicep' = {
  name: 'assign-acr-pull'
  scope: resourceGroup(acrResourceGroup)
  params: {
    principalId: userIdentity.properties.principalId
    acrName: acrName
  }
}

// 3. Create/Configure the Container App
resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: resourceGroup().location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: environmentId
    configuration: {
      registries: [
        {
          server: acrServer
          identity: userIdentity.id
        }
      ]
      ingress: {
        external: true
        targetPort: 8000
      }
    }
    template: {
      containers: [
        {
          name: containerAppName
          image: imageName
          resources: {
            cpu: json(cpu)
            memory: memory
          }
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }
    }
  }
  dependsOn: [       // This block ensures permissions are verified before the system pulls the image
    assignAcrPull 
  ]
}
