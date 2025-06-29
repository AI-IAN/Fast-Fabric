#\!/bin/bash
# Fabric Fast-Track deployment script

echo "Deploying Fabric Fast-Track infrastructure..."

# Set variables
RESOURCE_GROUP="rg-fabric-fasttrack"
LOCATION="eastus"
TEMPLATE="main.bicep"

# Create resource group if it doesn't exist
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy Bicep template
az deployment group create \
  --resource-group $RESOURCE_GROUP \
  --template-file $TEMPLATE \
  --parameters environmentPrefix=dev fabricSku=F2

echo "Deployment completed\!"
