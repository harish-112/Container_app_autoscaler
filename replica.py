import json
import subprocess

from config import (
    RESOURCE_GROUP,
    CONTAINER_APP_NAME
)

def get_current_replicas():

    command = [
        "az",
        "containerapp",
        "show",
        "--resource-group",RESOURCE_GROUP,
        "--name",CONTAINER_APP_NAME,
        "--query","properties.template.scale.minReplicas",
        "--output","json"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return int(json.loads(result.stdout))