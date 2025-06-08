from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from clients.azure import list_vms, get_cpu_metrics
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Put your subscription ID here or get from env var
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", "your-subscription-id")

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

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "vms": vms,
        "selected_vm": selected_vm,
        "cpu_metrics": cpu_metrics
    })
