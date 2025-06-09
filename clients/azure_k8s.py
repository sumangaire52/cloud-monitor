from azure.identity import AzureCliCredential
from azure.mgmt.containerservice import ContainerServiceClient
from kubernetes import client, config
import subprocess

credential = AzureCliCredential()


def get_aks_clusters(subscription_id: str):
    client_ = ContainerServiceClient(credential, subscription_id)
    clusters = []
    for cluster in client_.managed_clusters.list():
        clusters.append(
            {
                "name": cluster.name,
                "resource_group": cluster.id.split("/")[4],
                "location": cluster.location,
            }
        )
    return clusters


def configure_kube_client(resource_group: str, cluster_name: str):
    # Uses az CLI to update kubeconfig
    subprocess.run(
        [
            "az",
            "aks",
            "get-credentials",
            "--resource-group",
            resource_group,
            "--name",
            cluster_name,
            "--overwrite-existing",
        ],
        check=True,
    )
    config.load_kube_config()  # Load kube config to connect with client


def list_pods_with_metrics():
    v1 = client.CoreV1Api()
    metrics = client.CustomObjectsApi()

    pod_stats = []
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for pod in pods.items:
        pod_info = {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "node": pod.spec.node_name,
        }

        try:
            usage = metrics.get_namespaced_custom_object(
                group="metrics.k8s.io",
                version="v1beta1",
                namespace=pod.metadata.namespace,
                plural="pods",
                name=pod.metadata.name,
            )
            cpu = usage["containers"][0]["usage"]["cpu"]
            mem = usage["containers"][0]["usage"]["memory"]
            pod_info.update({"cpu": cpu, "memory": mem})
        except Exception:
            pod_info.update({"cpu": "N/A", "memory": "N/A"})

        pod_stats.append(pod_info)

    return pod_stats
