import json
import subprocess

from config import RESOURCE_ID

METRIC_MAP = {
    "CpuPercentage": "cpu",
    "MemoryPercentage": "memory",
    "Requests": "requests",
}

def get_metrics():
    command = [
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
        "monitor",
        "metrics",
        "list",
        "--resource",RESOURCE_ID,
        "--metric",",".join(METRIC_MAP.keys()),
        "--interval","PT5M",
        "--aggregation","Average",
        "--output","json"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    response = json.loads(result.stdout)
    metrics = {}

    for metric in response["value"]:

        name = metric["name"]["value"]
        value = None
        series = metric.get("timeseries", [])

        if series:
            data = series[0].get("data", [])
            if data:
                value = data[-1].get("average")

        metrics[METRIC_MAP.get(name)] = value

    return metrics