// Fabric Fast-Track Infrastructure Template
// Deploys complete Microsoft Fabric environment with Dev/Test/Prod workspaces
// Target: < 15 minute deployment with zero manual clicks

@description("Environment to deploy (dev, test, prod)")
@allowed(["dev", "test", "prod"])
param environment string = "dev"

@description("Organization prefix for naming resources")
param orgPrefix string = "fft"

@description("Microsoft Fabric capacity SKU - F2 minimum for Direct Lake")
@allowed(["F2", "F4", "F8", "F16", "F32", "F64", "F128", "F256", "F512"])
param fabricCapacitySku string = "F2"

@description("Azure region for deployment")
param location string = resourceGroup().location

@description("Fabric capacity administrator emails (semicolon separated)")
param fabricAdmins string = ""

@description("Deploy monitoring and alerting components")
param enableMonitoring bool = true

@description("Log Analytics workspace retention days")
param logRetentionDays int = 30

@description("SQL Server administrator password - should be passed from Key Vault or secure parameter")
@secure()
param sqlAdminPassword string

@description("Allowed IP addresses for SQL Server access (comma-separated)")
param sqlAllowedIpAddresses string = ""

// Variables for consistent naming
var namingPrefix = "${orgPrefix}-fabric-${environment}"
var adminEmails = split(fabricAdmins, ";")
var allowedIps = split(sqlAllowedIpAddresses, ",")

// Log Analytics Workspace for monitoring
resource logAnalyticsWorkspace "Microsoft.OperationalInsights/workspaces@2023-09-01" = if (enableMonitoring) {
  name: "${namingPrefix}-logs"
  location: location
  properties: {
    sku: {
      name: "PerGB2018"
    }
    retentionInDays: logRetentionDays
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// Application Insights for AI Assistant monitoring  
resource appInsights "Microsoft.Insights/components@2020-02-02" = if (enableMonitoring) {
  name: "${namingPrefix}-ai-insights"
  location: location
  kind: "web"
  properties: {
    Application_Type: "web"
    WorkspaceResourceId: enableMonitoring ? logAnalyticsWorkspace.id : null
  }
}

// Storage Account for data lake and staging
resource storageAccount "Microsoft.Storage/storageAccounts@2023-05-01" = {
  name: replace("${namingPrefix}storage", "-", "")
  location: location
  sku: {
    name: "Standard_LRS"
  }
  kind: "StorageV2"
  properties: {
    isHnsEnabled: true // Enable hierarchical namespace for Data Lake
    minimumTlsVersion: "TLS1_2"
    supportsHttpsTrafficOnly: true
    allowBlobPublicAccess: false
    accessTier: "Hot"
  }
}

// Data Lake containers for medallion architecture
resource bronzeContainer "Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01" = {
  name: "${storageAccount.name}/default/bronze"
  properties: {
    publicAccess: "None"
  }
}

resource silverContainer "Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01" = {
  name: "${storageAccount.name}/default/silver"
  properties: {
    publicAccess: "None"
  }
}

resource goldContainer "Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01" = {
  name: "${storageAccount.name}/default/gold"
  properties: {
    publicAccess: "None"
  }
}

// Key Vault for secrets management (AI Assistant keys, connection strings)
resource keyVault "Microsoft.KeyVault/vaults@2023-07-01" = {
  name: "${namingPrefix}-kv"
  location: location
  properties: {
    sku: {
      family: "A"
      name: "standard"
    }
    tenantId: tenant().tenantId
    enabledForDeployment: false
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: false
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    publicNetworkAccess: "Enabled"
    networkAcls: {
      defaultAction: "Allow"
      bypass: "AzureServices"
    }
  }
}

// Microsoft Fabric Capacity - Core infrastructure component
resource fabricCapacity "Microsoft.Fabric/capacities@2023-11-01" = {
  name: "${namingPrefix}-capacity"
  location: location
  sku: {
    name: fabricCapacitySku
    tier: "Fabric"
  }
  properties: {
    administration: {
      members: adminEmails
    }
  }
  tags: {
    Environment: environment
    Project: "Fabric-Fast-Track"
    CostCenter: "DataPlatform"
  }
}

// SQL Database for AI Assistant cost tracking and metadata
resource sqlServer "Microsoft.Sql/servers@2023-08-01-preview" = {
  name: "${namingPrefix}-sql"
  location: location
  properties: {
    administratorLogin: "fabricadmin"
    administratorLoginPassword: sqlAdminPassword
    version: "12.0"
    minimalTlsVersion: "1.2"
    publicNetworkAccess: "Disabled" // Use private endpoints for production
  }
}

resource sqlDatabase "Microsoft.Sql/servers/databases@2023-08-01-preview" = {
  parent: sqlServer
  name: "ai-assistant-db"
  location: location
  sku: {
    name: "Basic"
    tier: "Basic"
    capacity: 5
  }
  properties: {
    collation: "SQL_Latin1_General_CP1_CI_AS"
    maxSizeBytes: 2147483648 // 2GB
  }
}

// Firewall rule to allow Azure services (only if public access required)
resource sqlFirewallRuleAzure "Microsoft.Sql/servers/firewallRules@2023-08-01-preview" = if (sqlAllowedIpAddresses == "") {
  parent: sqlServer
  name: "AllowAzureServices"
  properties: {
    startIpAddress: "0.0.0.0"
    endIpAddress: "0.0.0.0"
  }
}

// Custom firewall rules for specific IP addresses
resource sqlFirewallRules "Microsoft.Sql/servers/firewallRules@2023-08-01-preview" = [for (ip, i) in allowedIps: if (ip != "") {
  parent: sqlServer
  name: "AllowIP${i}"
  properties: {
    startIpAddress: ip
    endIpAddress: ip
  }
}]

// Container Instance for AI Assistant (Streamlit UI)
resource containerGroup "Microsoft.ContainerInstance/containerGroups@2023-05-01" = {
  name: "${namingPrefix}-ai-assistant"
  location: location
  properties: {
    containers: [
      {
        name: "ai-assistant-ui"
        properties: {
          image: "python:3.11-slim"
          command: [
            "/bin/bash"
            "-c"
            "pip install streamlit pandas sqlalchemy && echo \"AI Assistant placeholder - implement Streamlit app\" && sleep infinity"
          ]
          ports: [
            {
              port: 8501
              protocol: "TCP"
            }
          ]
          resources: {
            requests: {
              cpu: 1
              memoryInGB: 2
            }
          }
          environmentVariables: [
            {
              name: "STREAMLIT_SERVER_PORT"
              value: "8501"
            }
            {
              name: "SQL_CONNECTION_STRING"
              secureValue: "Server=${sqlServer.properties.fullyQualifiedDomainName};Database=ai-assistant-db;User Id=fabricadmin;Password=${sqlAdminPassword};"
            }
            {
              name: "FABRIC_CAPACITY_ID"
              value: fabricCapacity.id
            }
          ]
        }
      }
    ]
    osType: "Linux"
    ipAddress: {
      type: "Public"
      ports: [
        {
          port: 8501
          protocol: "TCP"
        }
      ]
      dnsNameLabel: "${namingPrefix}-ai-assistant"
    }
    restartPolicy: "Always"
  }
}

// Action Group for monitoring alerts
resource actionGroup "Microsoft.Insights/actionGroups@2023-01-01" = if (enableMonitoring && fabricAdmins \!= "") {
  name: "${namingPrefix}-alerts"
  location: "Global"
  properties: {
    groupShortName: "FFTAlerts"
    enabled: true
    emailReceivers: [for (email, i) in adminEmails: {
      name: "admin${i}"
      emailAddress: email
      useCommonAlertSchema: true
    }]
  }
}

// Store important secrets in Key Vault
resource sqlConnectionStringSecret "Microsoft.KeyVault/vaults/secrets@2023-07-01" = {
  parent: keyVault
  name: "sql-connection-string"
  properties: {
    value: "Server=${sqlServer.properties.fullyQualifiedDomainName};Database=ai-assistant-db;User Id=fabricadmin;Password=${sqlAdminPassword};"
  }
}

resource storageConnectionStringSecret "Microsoft.KeyVault/vaults/secrets@2023-07-01" = {
  parent: keyVault
  name: "storage-connection-string"
  properties: {
    value: "DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net"
  }
}

// Outputs for pipeline and application configuration
output fabricCapacityId string = fabricCapacity.id
output fabricCapacityName string = fabricCapacity.name
output fabricCapacityEndpoint string = "https://api.fabric.microsoft.com/v1"
output storageAccountName string = storageAccount.name
output storageConnectionString string = "DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net"
output keyVaultName string = keyVault.name
output keyVaultUri string = keyVault.properties.vaultUri
output sqlServerName string = sqlServer.name
output sqlDatabaseName string = sqlDatabase.name
output aiAssistantUrl string = "http://${containerGroup.properties.ipAddress.fqdn}:8501"
output logAnalyticsWorkspaceId string = enableMonitoring ? logAnalyticsWorkspace.id : ""
output appInsightsInstrumentationKey string = enableMonitoring ? appInsights.properties.InstrumentationKey : ""
output deploymentTimestamp string = utcNow()
