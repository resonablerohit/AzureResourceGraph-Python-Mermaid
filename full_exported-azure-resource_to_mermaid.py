import os
import json
import pandas as pd

# 📁 Root folder where the JSON exports are stored
BASE_DIR = "./azure_exports"

# 🔄 Map of subfolders and files to load
json_sources = {
    "compute/vm.json": "VM",
    "network/nic.json": "NIC",
    "network/vnet.json": "VNET",
    "network/nsg.json": "NSG",
    "network/publicip.json": "PIP",
    "network/lb.json": "LB",
    "network/pe.json": "PE",
    "network/vnetpeering.json": "VNetPeering",
    "network/firewall.json": "Firewall",
    "network/appgateway.json": "AppGateway",
    "database/sqlservers.json": "SQL",
    "database/storage.json": "Storage",
    "web/appservices.json": "AppService",
    "web/appplans.json": "AppPlan",
    "identity/keyvault.json": "KeyVault",
    "identity/automation.json": "Automation",
}

# 📦 Load JSON data into memory
resources = {}
for rel_path, label in json_sources.items():
    path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(path):
        try:
            with open(path) as f:
                resources[label] = json.load(f)["data"]
        except Exception:
            print(f"⚠️ Could not load {label} from {rel_path}")
            resources[label] = []
    else:
        resources[label] = []

# 🔗 Build relationships
edges = []

# VM → NIC
for vm in resources.get("VM", []):
    vm_name = vm["name"]
    for nic_ref in vm.get("properties", {}).get("networkProfile", {}).get("networkInterfaces", []):
        nic_id = nic_ref.get("id", "")
        nic_name = nic_id.split("/")[-1]
        edges.append((vm_name, nic_name))

# NIC → Subnet → VNet
for nic in resources.get("NIC", []):
    nic_name = nic["name"]
    ip_configs = nic.get("properties", {}).get("ipConfigurations", [])
    for ip in ip_configs:
        subnet_id = ip.get("properties", {}).get("subnet", {}).get("id", "")
        if subnet_id:
            parts = subnet_id.split("/")
            vnet_name = parts[8] if len(parts) > 8 else "UnknownVNet"
            subnet_name = parts[10] if len(parts) > 10 else "UnknownSubnet"
            edges.append((nic_name, f"{vnet_name}_subnet_{subnet_name}"))

# NIC → NSG
for nic in resources.get("NIC", []):
    nic_name = nic["name"]
    nsg_id = nic.get("properties", {}).get("networkSecurityGroup", {}).get("id", "")
    if nsg_id:
        nsg_name = nsg_id.split("/")[-1]
        edges.append((nic_name, nsg_name))

# NIC → Public IP
for nic in resources.get("NIC", []):
    nic_name = nic["name"]
    ip_configs = nic.get("properties", {}).get("ipConfigurations", [])
    for ip in ip_configs:
        pip_id = ip.get("properties", {}).get("publicIPAddress", {}).get("id", "")
        if pip_id:
            pip_name = pip_id.split("/")[-1]
            edges.append((nic_name, pip_name))

# Private Endpoint → Subnet
for pe in resources.get("PE", []):
    pe_name = pe["name"]
    subnet_id = pe.get("properties", {}).get("subnet", {}).get("id", "")
    if subnet_id:
        parts = subnet_id.split("/")
        vnet_name = parts[8] if len(parts) > 8 else "UnknownVNet"
        subnet_name = parts[10] if len(parts) > 10 else "UnknownSubnet"
        edges.append((pe_name, f"{vnet_name}_subnet_{subnet_name}"))

# VNet Peering → Remote VNet
for peer in resources.get("VNetPeering", []):
    from_vnet = peer.get("properties", {}).get("remoteVirtualNetwork", {}).get("id", "").split("/")[-1]
    to_vnet = peer.get("name", "")
    if from_vnet and to_vnet:
        edges.append((from_vnet, to_vnet))

# Add one-hop service relationships
for service_type in ["AppService", "SQL", "Firewall", "AppGateway", "Storage", "KeyVault", "Automation", "AppPlan"]:
    for item in resources.get(service_type, []):
        edges.append((service_type, item["name"]))

# 🧩 Mermaid Diagram
mermaid_lines = ["```mermaid", "graph TD"]
for src, dst in edges:
    mermaid_lines.append(f"  {src} --> {dst}")
mermaid_lines.append("```")

# 💾 Output
output_file = os.path.join(BASE_DIR, "azure_topology_full.mmd")
with open(output_file, "w") as f:
    f.write("\n".join(mermaid_lines))

print(f"✅ Mermaid diagram exported to: {output_file}")
