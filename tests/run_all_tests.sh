#!/bin/bash
# Run all Fabric Fast-Track tests

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Fabric Fast-Track Test Suite ===${NC}"
echo ""

# Set test environment variables
export FABRIC_TENANT_ID="test-tenant-id"
export FABRIC_CLIENT_ID="test-client-id"
export FABRIC_CLIENT_SECRET="test-secret"
export WORKSPACE_NAME="Test-Workspace"

# Function to run a test suite
run_test() {
    local test_name=$1
    local test_file=$2

    echo -e "${YELLOW}Running: $test_name${NC}"
    if python3 "$test_file"; then
        echo -e "${GREEN}✅ $test_name PASSED${NC}"
        return 0
    else
        echo -e "${RED}❌ $test_name FAILED${NC}"
        return 1
    fi
    echo ""
}

# Track overall status
FAILED_TESTS=0

# Run deployment script tests
if ! run_test "Deployment Scripts Tests" "test_deployment_scripts.py"; then
    ((FAILED_TESTS++))
fi

# Run AI assistant tests (if exists)
if [ -f "../ai-assistant/test_ai_modules.py" ]; then
    if ! run_test "AI Assistant Tests" "../ai-assistant/test_ai_modules.py"; then
        ((FAILED_TESTS++))
    fi
fi

# Summary
echo ""
echo -e "${GREEN}=== Test Summary ===${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✅ All tests PASSED!${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED_TESTS test suite(s) FAILED${NC}"
    exit 1
fi
