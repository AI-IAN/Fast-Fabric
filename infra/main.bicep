// Fabric Fast-Track Infrastructure Template
// Deploys Dev/Test/Prod workspaces with F-SKU capacity

@description('Environment prefix (dev, test, prod)')
param environmentPrefix string = 'dev'

@description('Microsoft Fabric capacity SKU')
@allowed(['F2', 'F4', 'F8', 'F16', 'F32', 'F64'])
param fabricSku string = 'F2'

@description('Location for all resources')
param location string = resourceGroup().location

// Fabric Capacity
resource fabricCapacity 'Microsoft.Fabric/capacities@2023-11-01' = {
  name: 'fabric--capacity'
  location: location
  sku: {
    name: fabricSku
    tier: 'Fabric'
  }
  properties: {
    administration: {
      members: [
        // Add admin emails here
      ]
    }
  }
}

// Output capacity details
output capacityId string = fabricCapacity.id
output capacityName string = fabricCapacity.name
