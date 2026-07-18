import subprocess
from config import (
    RESOURCE_GROUP,
    BICEP_FILE
)

def update_replicas(target_replicas):

    command = [
    r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
    "deployment", "group", "create",
    "--resource-group", RESOURCE_GROUP,
    "--template-file", BICEP_FILE,
    "--parameters", "@parameters.json",  
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