from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from clients.azure import list_vms, get_cpu_metrics
from clients.azure_k8s import (
    get_aks_clusters,
    configure_kube_client,
    list_pods_with_metrics,
)
from settings import env
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", env.AZURE_SUBSCRIPTION_ID)


@app.get("/")
def home():
    # Redirect to dashboard for better UX
    return RedirectResponse("/dashboard")


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
def k8s_dashboard(request: Request, cluster: str = Query(None)):
    clusters = get_aks_clusters(SUBSCRIPTION_ID)
    selected_cluster = None
    pod_stats = []

    if cluster:
        selected_cluster = next((c for c in clusters if c["name"] == cluster), None)
        if selected_cluster:
            configure_kube_client(
                selected_cluster["resource_group"], selected_cluster["name"]
            )
            pod_stats = list_pods_with_metrics()

    return templates.TemplateResponse(
        "k8s_dashboard.html",
        {
            "request": request,
            "clusters": clusters,
            "selected_cluster": selected_cluster,
            "pod_stats": pod_stats,
        },
    )
