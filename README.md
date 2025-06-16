
# ☁️ Azure Cloud Monitoring Tool

A lightweight monitoring dashboard built with **FastAPI** to track **Azure Kubernetes Services (AKS)** and **Azure Virtual Machines (VMs)**. This tool fetches live metrics such as pod health, node status, VM CPU usage, and more—presented via a simple web interface.

---

## 🚀 Features

- 🔍 **AKS Cluster Monitoring**
  - List available AKS clusters
  - View pods and their CPU/Memory usage
  - Dynamically connect to AKS cluster using Kubernetes client

- 🖥️ **Azure VM Monitoring**
  - List all Virtual Machines in your subscription
  - View live CPU metrics using Azure Monitor

- 🧩 **Web Interface**
  - Clean, intuitive dashboards using Jinja2 templates
  - Query-based filtering (`?vm_name=...` / `?cluster=...`)

---

## 📸 Screenshots

*(Add screenshots here if available: dashboard UI, VM metrics chart, etc.)*

---

## 🏗️ Tech Stack

- **Backend**: FastAPI
- **Templates**: Jinja2
- **Cloud**: Azure SDK for Python
- **Kubernetes**: Python Kubernetes Client
- **Authentication**: Azure `DefaultAzureCredential`
- **Metrics**: Azure Monitor Metrics API

---

## 📁 Project Structure

```
cloud-monitor/
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── clients/
│   │   ├── azure.py           # VM listing & metric functions
│   │   └── azure_k8s.py       # AKS cluster & pod monitoring
│   ├── templates/
│   │   ├── dashboard.html     # VM dashboard
│   │   └── k8s_dashboard.html # AKS dashboard
│   └── settings.py            # Environment loading
├── .env                       # Azure credentials and config
├── requirements.txt
└── README.md
```

---

## 🔐 Prerequisites

- Python 3.9+
- An active Azure subscription
- Azure resources:
  - At least one AKS cluster
  - One or more Virtual Machines
- Service Principal or User with sufficient permissions

---

## ⚙️ Environment Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/cloud-monitor.git
   cd cloud-monitor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file or export manually:

   ```env
   AZURE_SUBSCRIPTION_ID=your-azure-subscription-id
   ```

4. **Login to Azure**
   ```bash
   az login
   ```

---

## ▶️ Run the App

```bash
uvicorn app.main:app --reload
```

Visit:
- 🖥️ http://localhost:8000/dashboard — for VM Monitoring
- ☸️ http://localhost:8000/k8s-dashboard — for AKS Monitoring

---

## 📦 Example API Queries

- VM Dashboard:
  ```
  /dashboard?vm_name=my-vm
  ```

- K8s Dashboard:
  ```
  /k8s-dashboard?cluster=my-aks-cluster
  ```

---

## 🛡️ Security Tips

- Do not hardcode credentials — use `.env` or Azure-managed identities.
- Add API key protection or OAuth2 if deploying publicly.
- Avoid exposing metrics endpoints without auth.

---

## 🧪 Testing (Optional)

You can write unit tests using `pytest` for:
- Azure client methods (mocked)
- FastAPI route responses
- Jinja template context

---

## 🐳 Docker (Optional)

```Dockerfile
FROM python:3.11

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🙌 Acknowledgments

- [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Kubernetes Python Client](https://github.com/kubernetes-client/python)

---

## 📃 License

MIT — free to use, modify, and share.

---

## ✨ Author

**Suman Gaire**
📧 sumangaire52@gmail.com
🌐 [LinkedIn](https://linkedin.com/in/sumangaire) | [GitHub](https://github.com/sumangaire52)
