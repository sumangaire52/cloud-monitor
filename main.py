from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates

from clients.azure import list_vms, get_cpu_metrics
from clients.azure_k8s import (
    get_aks_clusters,
    configure_kube_client,
    list_pods_with_metrics,
    list_namespaces,
)
from settings import env
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", env.AZURE_SUBSCRIPTION_ID)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard")
def dashboard(request: Request, vm_name: str = Query(None)):
    vms = list_vms(SUBSCRIPTION_ID)
    selected_vm = None
    cpu_metrics = []

    if vm_name:
        # Find VM resource ID
        selected_vm = next((vm for vm in vms if vm["name"] == vm_name), None)
        if selected_vm:
            cpu_metrics = get_cpu_metrics(selected_vm["id"])

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "vms": vms,
            "selected_vm": selected_vm,
            "cpu_metrics": cpu_metrics,
        },
    )


@app.get("/k8s-dashboard")
def k8s_dashboard(
    request: Request, cluster: str = Query(None), namespace: str = Query(None)
):
    clusters = get_aks_clusters(subscription_id=SUBSCRIPTION_ID)
    selected_cluster = None
    pod_stats = []
    namespaces = []

    if cluster:
        selected_cluster = next((c for c in clusters if c["name"] == cluster), None)
        if selected_cluster:
            configure_kube_client(
                selected_cluster["resource_group"], selected_cluster["name"]
            )
            namespaces = list_namespaces(
                selected_cluster["resource_group"], selected_cluster["name"]
            )

            if namespace:
                pod_stats = list_pods_with_metrics(namespace=namespace)

    return templates.TemplateResponse(
        "k8s_dashboard.html",
        {
            "request": request,
            "clusters": clusters,
            "selected_cluster": selected_cluster,
            "namespace": namespace,
            "namespaces": namespaces,
            "pod_stats": pod_stats,
        },
    )
