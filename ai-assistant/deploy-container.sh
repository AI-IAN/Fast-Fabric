#!/bin/bash
# Deploy AI Assistant Container to Azure
# This script builds, pushes, and deploys the Streamlit AI Assistant

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Fabric Fast-Track AI Assistant Container Deployment ===${NC}"

# Configuration
ACR_NAME="${1:-your-acr-name}"
IMAGE_NAME="fabric-ai-assistant"
IMAGE_TAG="${2:-latest}"
FULL_IMAGE="${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}"

if [ "$ACR_NAME" == "your-acr-name" ]; then
    echo -e "${YELLOW}Usage: ./deploy-container.sh <acr-name> [tag]${NC}"
    echo -e "${YELLOW}Example: ./deploy-container.sh myacr v1.0${NC}"
    exit 1
fi

echo -e "${GREEN}Building Docker image...${NC}"
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f Dockerfile ..

echo -e "${GREEN}Tagging image for ACR...${NC}"
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${FULL_IMAGE}

echo -e "${GREEN}Logging into Azure Container Registry...${NC}"
az acr login --name ${ACR_NAME}

echo -e "${GREEN}Pushing image to ACR...${NC}"
docker push ${FULL_IMAGE}

echo -e "${GREEN}✅ Container image deployed successfully!${NC}"
echo -e "${GREEN}Image: ${FULL_IMAGE}${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update infra/main.bicep container image reference to: ${FULL_IMAGE}"
echo "2. Grant ACI access to ACR (if not already done):"
echo "   az role assignment create --assignee <aci-identity> --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.ContainerRegistry/registries/${ACR_NAME} --role AcrPull"
echo "3. Deploy infrastructure:"
echo "   cd ../infra && ./deploy.sh -e dev -g <resource-group> -s <subscription-id>"
