from datetime import timedelta

from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient, MetricAggregationType

from config import RESOURCE_ID 

credential = DefaultAzureCredential()
client = MetricsQueryClient(credential)

resource_id = RESOURCE_ID

def get_metrics():

    response = client.query_resource(
        resource_uri=resource_id,
        metric_names=[
            "CpuPercentage",
            "MemoryPercentage",
            "Requests",
            "Replicas"
        ],
        timespan=timedelta(minutes=5),
        aggregations=[MetricAggregationType.AVERAGE]
    )

    metrics = {}

    for metric in response.metrics:
        value = None
        for series in metric.timeseries:
            if series.data:
                latest = series.data[-1]
                value = latest.average
                break
        metrics[metric.name] = value

    return metrics


if __name__ == "__main__":
    metrics = get_metrics()
    print(metrics)