#!/bin/bash

echo "🔄 Starting Azure Resource Graph export..."
echo "🕒 $(date)"

# Create structured export directories
mkdir -p azure_exports/{compute,network,database,web,identity,governance,summary}
cd azure_exports

##############################
# 🖥️ Compute & Core Networking
##############################
echo "🔹 Exporting Compute & Core Network Resources"
az graph query -q "Resources | where type =~ 'Microsoft.Compute/virtualMachines'" --output json > compute/vm.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/networkInterfaces'" --output json > network/nic.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/virtualNetworks'" --output json > network/vnet.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/networkSecurityGroups'" --output json > network/nsg.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/publicIPAddresses'" --output json > network/publicip.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/loadBalancers'" --output json > network/lb.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/privateEndpoints'" --output json > network/pe.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/virtualNetworkPeerings'" --output json > network/vnetpeering.json

################################
# 🌐 App Delivery & Firewalls
################################
echo "🔹 Exporting Application Delivery & Firewall Resources"
az graph query -q "Resources | where type =~ 'Microsoft.Network/applicationGateways'" --output json > network/appgateway.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/azureFirewalls'" --output json > network/firewall.json
az graph query -q "Resources | where type =~ 'Microsoft.Cdn/profiles'" --output json > network/cdn.json
az graph query -q "Resources | where type =~ 'Microsoft.FrontDoor/frontDoors'" --output json > network/frontdoor.json
az graph query -q "Resources | where type =~ 'Microsoft.Network/networkWatchers'" --output json > network/networkwatcher.json

#########################
# 🗄️ Storage & Databases
#########################
echo "🔹 Exporting Storage & Database Resources"
az graph query -q "Resources | where type =~ 'Microsoft.Storage/storageAccounts'" --output json > database/storage.json
az graph query -q "Resources | where type =~ 'Microsoft.Sql/servers'" --output json > database/sqlservers.json
az graph query -q "Resources | where type =~ 'Microsoft.Sql/servers/databases'" --output json > database/sqldb.json
az graph query -q "Resources | where type =~ 'Microsoft.DBforPostgreSQL/servers'" --output json > database/postgres.json
az graph query -q "Resources | where type =~ 'Microsoft.DBforMySQL/servers'" --output json > database/mysql.json
az graph query -q "Resources | where type =~ 'Microsoft.DocumentDB/databaseAccounts'" --output json > database/cosmos.json

######################
# 🧩 Web & Identity
######################
echo "🔹 Exporting Web & Identity Resources"
az graph query -q "Resources | where type =~ 'Microsoft.Web/sites'" --output json > web/appservices.json
az graph query -q "Resources | where type =~ 'Microsoft.Web/serverFarms'" --output json > web/appplans.json
az graph query -q "Resources | where type =~ 'Microsoft.Automation/automationAccounts'" --output json > identity/automation.json
az graph query -q "Resources | where type =~ 'Microsoft.ManagedIdentity/userAssignedIdentities'" --output json > identity/managedidentities.json
az graph query -q "Resources | where type =~ 'Microsoft.KeyVault/vaults'" --output json > identity/keyvault.json

##############################
# 🛡️ Governance & Tagging
##############################
echo "🔹 Exporting Governance Resources"
az graph query -q "Resources | where type =~ 'Microsoft.Resources/tags'" --output json > governance/tags.json
az graph query -q "Resources | where type =~ 'Microsoft.Resources/resourceGroups'" --output json > governance/resourcegroups.json
az graph query -q "ResourceContainers | where type == 'microsoft.resources/subscriptions'" --output json > governance/subscriptions.json

################################
# 📊 Summary Table (by type)
################################
az graph query -q "Resources | summarize count() by type" --output table > summary/resource_counts.txt

echo "✅ Export complete. Output saved in ./azure_exports/"
echo "🕓 Finished: $(date)"
