import os
from dotenv import load_dotenv
load_dotenv()

SUBSCRIPTION_ID=os.getenv("SUBSCRIPTION_ID")
RESOURCE_GROUP=os.getenv("RESOURCE_GROUP")
CONTAINER_APP_NAME=os.getenv("CONTAINER_APP_NAME")
ENVIRONMENT_ID = os.getenv("ENVIRONMENT_ID")
IMAGE_NAME = os.getenv("IMAGE_NAME")
RESOURCE_ID = (
    f"/subscriptions/{SUBSCRIPTION_ID}"
    f"/resourceGroups/{RESOURCE_GROUP}"
    f"/providers/Microsoft.App/containerApps/{CONTAINER_APP_NAME}"
)

TARGET_CPU=75
MIN_REPLICAS=1
MAX_REPLICAS=5
CHECK_INTERVAL=20
COOLDOWN=60
SCALE_CONFIRMATION_COUNT=2
BICEP_FILE = "deploy.bicep"

