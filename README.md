# AzureResourceGraph-Python-Mermaid
Azure Resource Graph + Python + Mermaid – Automated Azure Infrastructure Visualization 
This solution provides a robust and automated approach to visualize Azure infrastructure by combining the capabilities of Azure Resource Graph, Python, and Mermaid.

Using Azure Resource Graph (ARG), we perform efficient and scalable queries across Azure subscriptions to collect metadata about deployed resources. This includes details about resource types, configurations, relationships, and dependencies—making it highly useful for multi-subscription or enterprise-scale environments.

Once the data is extracted via az graph query, it is parsed and processed using Python. Python scripts clean, normalize, and map the resources into logical relationships—such as virtual machines connected to NICs, subnets, public IPs, load balancers, and more. This step also supports filtering, categorization, and transformation of resource properties into meaningful graph structures.

The structured data is then rendered using Mermaid, a JavaScript-based diagramming tool that supports markdown-style syntax. Mermaid allows us to programmatically generate infrastructure diagrams such as flowcharts, dependency trees, and layered network maps
