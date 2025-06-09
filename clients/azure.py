from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.monitor.query import MetricsQueryClient
from datetime import datetime, timedelta

credential = AzureCliCredential()


def get_compute_client(subscription_id: str):
    return ComputeManagementClient(credential, subscription_id)


def get_metrics_client():
    return MetricsQueryClient(credential)


def list_vms(subscription_id: str):
    client = get_compute_client(subscription_id)
    vms = []
    for vm in client.virtual_machines.list_all():
        vms.append(
            {
                "name": vm.name,
                "resource_group": vm.id.split("/")[4],  # extract RG from resource ID
                "location": vm.location,
                "id": vm.id,
            }
        )
    return vms


def get_cpu_metrics(resource_id: str):
    client = get_metrics_client()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    response = client.query_resource(
        resource_id,
        metric_names=["Percentage CPU"],
        timespan=(start_time, end_time),
        granularity=timedelta(minutes=5),
        aggregations=["Average"],
    )

    # Extract data points for the metric
    cpu_points = []
    for metric in response.metrics:
        for time_series_element in metric.timeseries:
            for data in time_series_element.data:
                if data.average is not None:
                    cpu_points.append(
                        {"time": data.timestamp.isoformat(), "average": data.average}
                    )

    return cpu_points
