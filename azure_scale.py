import subprocess
from config import (
    RESOURCE_GROUP,
    BICEP_FILE
)

def update_replicas(target_replicas):
    """
    I designed this function to execute the actual scaling infrastructure updates in Azure. 
    
    While using `az containerapp update` would be the standard way to quickly bump up the replica count, 
    the project explicitly demands infrastructure automation using Bicep. To keep everything strictly 
    aligned with the IaC framework, I chose to use `az deployment group create` instead. 
    
    By passing the target replica numbers directly as Bicep parameters, I ensure that the code 
    remains completely declarative, reusable, and manages the entire app configuration in a single, 
    state-consistent deployment.
    """

    command = [
    r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
    "deployment", "group", "create",
    "--resource-group", RESOURCE_GROUP,
    "--template-file", BICEP_FILE,
    "--parameters", "@bicep/parameters.json",  
    "--parameters", f"minReplicas={target_replicas}", f"maxReplicas={target_replicas}" 
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("Successfully deployed with Replicas = ", target_replicas)

    else:
        print(result.stderr)