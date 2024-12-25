# Python Application Deployment on EKS

This project demonstrates deploying a simple Python application on Amazon Elastic Kubernetes Service (EKS). The application is built using Flask and is containerized using Docker. The Kubernetes deployment includes a service to expose the application.

## Features
- A Flask-based Python app.
- Dockerized application with a lightweight `python:3.9-slim` image.
- Kubernetes deployment and service configurations.
- Runs on EKS.

## Files

- **`app.py`**: The Flask application.
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

## AWS EKS Setup

### 1. Create an EKS Cluster

Use `eksctl` to create an EKS cluster with the necessary node groups.

```bash
# Create EKS cluster
eksctl create cluster \
  --name flask-rps-cluster \
  --version 1.26 \
  --region <your-region> \
  --nodegroup-name flask-rps-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```

#### Explanation:
- **`--name`**: Specifies the name of the cluster.
- **`--version`**: Kubernetes version for the cluster.
- **`--region`**: AWS region where the cluster will be created.
- **`--nodegroup-name`**: Name of the managed node group.
- **`--node-type`**: Instance type for the nodes (e.g., `t3.medium`).
- **`--nodes`**: Number of desired nodes (initial size).
- **`--nodes-min` / `--nodes-max`**: Auto-scaling configuration for the node group.
- **`--managed`**: Uses managed node groups for easier management.

---

### 2. Configure `kubectl` to Connect to the Cluster

After creating the cluster, update your `kubeconfig` file:

```bash
aws eks --region <your-region> update-kubeconfig --name flask-rps-cluster
```

Verify connection to the cluster:

```bash
kubectl get nodes
```

---

### 3. Deploy the Flask App

#### Step 1: Apply the Deployment Manifest

Save the following deployment manifest to `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-rps-deployment
  labels:
    app: flask-rps
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-rps
  template:
    metadata:
      labels:
        app: flask-rps
    spec:
      containers:
      - name: flask-rps
        image: ibraheemcisse/flask-rps-app:latest
        ports:
        - containerPort: 5000
```

Apply it using:

```bash
kubectl apply -f deployment.yaml
```

#### Step 2: Apply the Service Manifest

Save the following service manifest to `service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-rps-service
spec:
  type: LoadBalancer
  selector:
    app: flask-rps
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
```

Apply it using:

```bash
kubectl apply -f service.yaml
```

---

### 4. Access the Application

Once the `LoadBalancer` service is deployed, get its external IP:

```bash
kubectl get svc
```

Access your app at `http://<external-ip>`.

---

---

## Future Enhancements
- Add Horizontal Pod Autoscaler (HPA) for scaling.
- Implement an Ingress resource for better traffic management.
- Enhance security with NetworkPolicies and Secrets.
