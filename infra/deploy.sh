#\!/bin/bash
# Fabric Fast-Track Infrastructure Deployment Script
# Target: < 15 minute deployment with zero manual clicks

set -e  # Exit on any error

# Color coding for output
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

# Default values
ENVIRONMENT="dev"
RESOURCE_GROUP=""
LOCATION="eastus"
SUBSCRIPTION_ID=""
VALIDATE_ONLY=false

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -e, --environment     Environment to deploy (dev, test, prod) [default: dev]"
    echo "  -g, --resource-group  Resource group name (required)"
    echo "  -l, --location        Azure region [default: eastus]"
    echo "  -s, --subscription    Azure subscription ID (required)"
    echo "  -v, --validate        Validate template only, do not deploy"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -g rg-fabric-dev -s 12345678-1234-1234-1234-123456789012"
    echo "  $0 -e prod -g rg-fabric-prod -s 12345678-1234-1234-1234-123456789012"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -g|--resource-group)
            RESOURCE_GROUP="$2"
            shift 2
            ;;
        -l|--location)
            LOCATION="$2"
            shift 2
            ;;
        -s|--subscription)
            SUBSCRIPTION_ID="$2"
            shift 2
            ;;
        -v|--validate)
            VALIDATE_ONLY=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$RESOURCE_GROUP" ]]; then
    print_error "Resource group is required. Use -g or --resource-group"
    show_usage
    exit 1
fi

if [[ -z "$SUBSCRIPTION_ID" ]]; then
    print_error "Subscription ID is required. Use -s or --subscription"
    show_usage
    exit 1
fi

# Validate environment
if [[ "$ENVIRONMENT" \!= "dev" && "$ENVIRONMENT" \!= "test" && "$ENVIRONMENT" \!= "prod" ]]; then
    print_error "Environment must be dev, test, or prod"
    exit 1
fi

print_status "=== Fabric Fast-Track Infrastructure Deployment ==="
print_status "Environment: $ENVIRONMENT"
print_status "Resource Group: $RESOURCE_GROUP"
print_status "Location: $LOCATION"
print_status "Subscription: $SUBSCRIPTION_ID"
print_status "Validate Only: $VALIDATE_ONLY"

# Check if Azure CLI is installed and logged in
if \! command -v az &> /dev/null; then
    print_error "Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if logged in to Azure
if \! az account show &> /dev/null; then
    print_error "Not logged in to Azure. Please run az login first."
    exit 1
fi

# Set subscription
print_status "Setting Azure subscription..."
az account set --subscription "$SUBSCRIPTION_ID"

# Create resource group if it does not exist
print_status "Creating resource group if it does not exist..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none

# Check if parameter file exists
PARAM_FILE="parameters.${ENVIRONMENT}.json"
if [[ \! -f "$PARAM_FILE" ]]; then
    print_error "Parameter file $PARAM_FILE not found"
    exit 1
fi

print_status "Using parameter file: $PARAM_FILE"

# Record start time
START_TIME=$(date +%s)

if [[ "$VALIDATE_ONLY" == true ]]; then
    print_status "Validating Bicep template..."
    az deployment group validate \
        --resource-group "$RESOURCE_GROUP" \
        --template-file main.bicep \
        --parameters @"$PARAM_FILE" \
        --output table
    
    if [[ $? -eq 0 ]]; then
        print_success "Template validation successful\!"
    else
        print_error "Template validation failed\!"
        exit 1
    fi
else
    print_status "Deploying Fabric Fast-Track infrastructure..."
    print_status "This may take 10-15 minutes..."
    
    # Deploy with detailed output
    DEPLOYMENT_NAME="fabric-deployment-$(date +%Y%m%d-%H%M%S)"
    
    az deployment group create \
        --resource-group "$RESOURCE_GROUP" \
        --template-file main.bicep \
        --parameters @"$PARAM_FILE" \
        --name "$DEPLOYMENT_NAME" \
        --output json > deployment_output.json
    
    DEPLOY_STATUS=$?
    
    # Calculate deployment time
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    
    if [[ $DEPLOY_STATUS -eq 0 ]]; then
        print_success "Deployment completed successfully\!"
        print_success "Deployment time: ${MINUTES}m ${SECONDS}s"
        
        # Check if deployment was within target time
        if [[ $MINUTES -lt 15 ]]; then
            print_success "🎯 TARGET MET: Deployment completed in under 15 minutes\!"
        else
            print_warning "⚠️  TARGET MISSED: Deployment took longer than 15 minutes"
        fi
        
        print_success "Fabric Fast-Track infrastructure is ready\!"
    else
        print_error "Deployment failed\!"
        print_error "Deployment time: ${MINUTES}m ${SECONDS}s"
        exit 1
    fi
fi

print_success "Script completed successfully\!"
