# Python App on EKS

This project demonstrates deploying a simple Python application on Amazon Elastic Kubernetes Service (EKS). The application is built using Flask, and is containerized using Docker. The Kubernetes deployment includes a service to expose the application.

## Features
- A Flask-based Python app with Prometheus metrics.
- Dockerized application with a lightweight `python:3.9-slim` image.
- Kubernetes deployment and service configurations.
- Runs on EKS.

## Files

- **`app.py`**: The Flask application with Prometheus metrics.
- **`Dockerfile`**: Instructions for building the Docker image.
- **`requirements.txt`**: Python dependencies.
- **`deployment.yaml`**: Kubernetes Deployment manifest.
- **`service.yaml`**: Kubernetes Service manifest.
- **`get_helm.sh`**: Helper script for setting up Helm (optional).

---

## Prerequisites

1. **Amazon EKS Cluster**: Set up an EKS cluster and configure `kubectl` to connect to it.
2. **Docker**: Install Docker to build the container image.
3. **kubectl**: Ensure you have the Kubernetes command-line tool installed.
4. **Helm** (optional): If needed for additional setup tools.

---

## Steps to Deploy

### 1. Clone the Repository
```bash
# Clone the repository
$ git clone <repository-url>
$ cd <repository-folder>
```

### 2. Build and Push Docker Image
Update the Docker Hub username in the `image` field of `deployment.yaml` if necessary.
```bash
# Build Docker image
$ docker build -t <docker-hub-username>/flask-rps-app:latest .

# Push image to Docker Hub
$ docker push <docker-hub-username>/flask-rps-app:latest
```

### 3. Deploy to Kubernetes

#### Apply Deployment Manifest
```bash
$ kubectl apply -f deployment.yaml
```

#### Apply Service Manifest
```bash
$ kubectl apply -f service.yaml
```

### 4. Access the Application

Find the node's external IP and access the application via the `NodePort`.
```bash
$ kubectl get nodes -o wide
$ kubectl get svc
```

Access the app:
- **App Endpoint**: `http://<node-ip>:30000`
- **Prometheus Metrics**: `http://<node-ip>:30000/metrics`

---

## Application Overview

### Flask Application (`app.py`)
- **Endpoints**:
  - `/`: Returns `Hello, World!`

### Dockerfile
- Uses `python:3.9-slim` for a lightweight container.
- Installs dependencies listed in `requirements.txt`.
- Exposes port 80 and runs the Flask app.

### Kubernetes Configuration
- **Deployment (`deployment.yaml`)**:
  - Single replica of the app.
  - Resource requests and limits defined.
  - Uses the Docker image built earlier.
- **Service (`service.yaml`)**:
  - NodePort service to expose the app on port `30000`.

---

## Clean Up
To delete the deployment and service:
```bash
$ kubectl delete -f deployment.yaml
$ kubectl delete -f service.yaml
```

---

## Future Enhancements
- Add Horizontal Pod Autoscaler (HPA) for scaling based on metrics.
- Implement an Ingress resource for better traffic management.
- Enhance security with NetworkPolicies and Secrets.
