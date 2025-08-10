# Python Flask Application Deployment on Amazon EKS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.26+-blue.svg)](https://kubernetes.io/)
[![AWS EKS](https://img.shields.io/badge/AWS-EKS-orange.svg)](https://aws.amazon.com/eks/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-20.0+-blue.svg)](https://www.docker.com/)

A comprehensive guide to deploying a production-ready Python Flask application on Amazon Elastic Kubernetes Service (EKS). This project demonstrates containerization, Kubernetes deployment patterns, and AWS cloud-native best practices.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/ibraheemcisse/Python-Application-Deployment-on-Amazon-Elastic-Kubernetes-Service-EKS-.git
cd Python-Application-Deployment-on-Amazon-Elastic-Kubernetes-Service-EKS-

# Create EKS cluster
eksctl create cluster -f cluster-config.yaml

# Deploy the application
kubectl apply -f k8s/
```

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Accessing the Application](#-accessing-the-application)
- [Monitoring & Scaling](#-monitoring--scaling)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)

## 🎯 Overview

This project showcases a **production-ready deployment** of a Python Flask application on Amazon EKS, demonstrating:

- **Container Best Practices**: Multi-stage Docker builds with security hardening
- **Kubernetes Patterns**: Proper resource management, health checks, and scaling
- **AWS Integration**: EKS cluster configuration with managed node groups
- **Production Readiness**: Security contexts, resource limits, and monitoring

### Key Features

- ✅ **High Availability**: Multiple replicas with proper distribution
- ✅ **Auto Scaling**: Horizontal Pod Autoscaler based on CPU/memory
- ✅ **Security**: Non-root containers with security contexts
- ✅ **Monitoring**: Health checks and resource monitoring
- ✅ **Production Ready**: Resource limits, proper networking, and error handling

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Internet      │    │   Application    │    │   EKS Cluster   │
│   Gateway       │────│   Load Balancer  │────│   (2-3 Nodes)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Flask Service  │    │   Worker Nodes  │
                       │   (Port 80)      │    │   (t3.medium)   │
                       └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Flask Pods     │    │   Pod Replicas  │
                       │   (2-10 replicas)│    │   (Auto-scaled) │
                       └──────────────────┘    └─────────────────┘
```

### Components

| Component | Purpose | Configuration |
|-----------|---------|---------------|
| **Flask Application** | Python web service | Port 5000, health endpoints |
| **EKS Cluster** | Kubernetes orchestration | 1.26+, managed node groups |
| **Load Balancer** | External traffic distribution | AWS ALB/NLB integration |
| **Auto Scaler** | Dynamic scaling | CPU/memory based triggers |

## 📦 Prerequisites

### Required Tools

Install these tools before proceeding:

- **AWS CLI** (v2.x) - [Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- **eksctl** (v0.140+) - [Installation Guide](https://eksctl.io/installation/)
- **kubectl** (v1.26+) - [Installation Guide](https://kubernetes.io/docs/tasks/tools/)
- **Docker** (v20.x+) - [Installation Guide](https://docs.docker.com/get-docker/)

### AWS Requirements

- **AWS Account** with programmatic access
- **IAM Permissions** for EKS, EC2, VPC, and LoadBalancer operations
- **AWS CLI** configured with appropriate credentials

```bash
# Verify AWS configuration
aws sts get-caller-identity
aws eks list-clusters
```

### System Requirements

- **Memory**: 4GB RAM minimum (8GB recommended)
- **CPU**: 2+ cores for local development
- **Storage**: 5GB available disk space
- **Network**: Reliable internet connection

## 🛠️ Installation

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/ibraheemcisse/Python-Application-Deployment-on-Amazon-Elastic-Kubernetes-Service-EKS-.git
cd Python-Application-Deployment-on-Amazon-Elastic-Kubernetes-Service-EKS-

# Make scripts executable
chmod +x scripts/*.sh
```

### Step 2: Create EKS Cluster

Using the enhanced cluster configuration:

```bash
# Create cluster with optimized settings
eksctl create cluster -f cluster-config.yaml

# Verify cluster creation
kubectl get nodes
kubectl get pods --all-namespaces
```

### Step 3: Build and Push Docker Image (Optional)

If you want to build your own image:

```bash
# Build the Docker image
docker build -t your-registry/flask-app:v1.0.0 .

# Push to your container registry
docker push your-registry/flask-app:v1.0.0

# Update deployment.yaml with your image
```

## ⚙️ Configuration

### Environment Variables

The Flask application supports these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment (development/production) |
| `FLASK_DEBUG` | `False` | Enable/disable debug mode |
| `PORT` | `5000` | Port for the Flask application |
| `WORKERS` | `4` | Number of Gunicorn workers |

### Kubernetes Configuration

Key configuration files and their purposes:

- `cluster-config.yaml` - EKS cluster specifications
- `k8s/namespace.yaml` - Namespace isolation
- `k8s/deployment.yaml` - Application deployment with best practices
- `k8s/service.yaml` - Service exposure configuration
- `k8s/hpa.yaml` - Horizontal Pod Autoscaler
- `k8s/ingress.yaml` - Ingress controller configuration

## 🚀 Deployment

### Deploy All Resources

```bash
# Apply all Kubernetes manifests
kubectl apply -f k8s/

# Verify deployment status
kubectl get all -n flask-app
```

### Step-by-Step Deployment

If you prefer to deploy resources individually:

```bash
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Deploy the application
kubectl apply -f k8s/deployment.yaml

# 3. Create service
kubectl apply -f k8s/service.yaml

# 4. Enable auto-scaling
kubectl apply -f k8s/hpa.yaml

# 5. Configure ingress (optional)
kubectl apply -f k8s/ingress.yaml
```

### Verify Deployment

```bash
# Check pod status
kubectl get pods -n flask-app

# Check service endpoints
kubectl get svc -n flask-app

# Check auto-scaler status
kubectl get hpa -n flask-app

# View application logs
kubectl logs -f deployment/flask-app -n flask-app
```

## 🌐 Accessing the Application

### Get External Access

```bash
# Get LoadBalancer external IP
kubectl get svc flask-service -n flask-app

# Wait for EXTERNAL-IP to be assigned (may take 2-3 minutes)
# Access at: http://<EXTERNAL-IP>
```

### Port Forwarding (Development)

```bash
# Forward local port to service
kubectl port-forward svc/flask-service -n flask-app 8080:80

# Access at: http://localhost:8080
```

### Available Endpoints

- `GET /` - Application home page
- `GET /health` - Health check endpoint
- `GET /ready` - Readiness probe endpoint
- `GET /metrics` - Basic application metrics

## 📊 Monitoring & Scaling

### Horizontal Pod Autoscaling

The HPA automatically scales pods based on resource usage:

```bash
# Check current scaling status
kubectl get hpa -n flask-app

# Watch scaling events
kubectl get events --sort-by=.lastTimestamp -n flask-app

# Test scaling with load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
```

### Monitoring Commands

```bash
# Monitor resource usage
kubectl top pods -n flask-app
kubectl top nodes

# View detailed pod information
kubectl describe pod <pod-name> -n flask-app

# Check cluster events
kubectl get events --sort-by=.lastTimestamp
```

### Load Testing

Simple load test to trigger scaling:

```bash
# Install siege for load testing
# On macOS: brew install siege
# On Ubuntu: sudo apt-get install siege

# Run load test
siege -c 20 -t 2M http://<EXTERNAL-IP>
```

## 🔒 Security

### Security Features Implemented

1. **Container Security**:
   - Non-root user execution
   - Read-only root filesystem
   - Dropped capabilities
   - Security context enforcement

2. **Network Security**:
   - Namespace isolation
   - Service-to-service communication
   - LoadBalancer with AWS security groups

3. **Resource Security**:
   - Resource limits and requests
   - CPU and memory constraints
   - Proper RBAC (future enhancement)

### Security Best Practices

```bash
# Scan for security vulnerabilities
kubectl auth can-i --list --as=system:serviceaccount:flask-app:default

# Check security contexts
kubectl get pods -n flask-app -o jsonpath='{.items[*].spec.securityContext}'

# Review resource limits
kubectl describe resourcequota -n flask-app
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Pods Not Starting

```bash
# Check pod status and events
kubectl describe pod <pod-name> -n flask-app

# Common causes:
# - Image pull errors: Check image name and registry access
# - Resource constraints: Check node capacity
# - Configuration errors: Validate YAML syntax
```

#### 2. Service Not Accessible

```bash
# Verify service configuration
kubectl get svc -n flask-app -o wide

# Check endpoints
kubectl get endpoints -n flask-app

# Test internal connectivity
kubectl run test-pod --image=busybox -i --tty --rm -- /bin/sh
# Inside pod: wget -qO- http://flask-service.flask-app.svc.cluster.local
```

#### 3. Auto-scaling Not Working

```bash
# Check HPA status
kubectl describe hpa flask-app-hpa -n flask-app

# Verify metrics server
kubectl get deployment metrics-server -n kube-system

# Check resource usage
kubectl top pods -n flask-app
```

#### 4. LoadBalancer Pending

```bash
# Check AWS LoadBalancer Controller
kubectl get pods -n kube-system | grep aws-load-balancer

# Verify service annotations
kubectl describe svc flask-service -n flask-app

# Check AWS console for LoadBalancer creation
```

### Debug Commands

```bash
# Get comprehensive cluster info
kubectl cluster-info dump

# Check all resources in namespace
kubectl get all -n flask-app

# View recent events
kubectl get events --sort-by=.lastTimestamp -n flask-app

# Export resource configurations
kubectl get deployment flask-app -n flask-app -o yaml > debug-deployment.yaml
```

## ✅ Best Practices

### Container Best Practices

- **Multi-stage builds** for smaller, secure images
- **Non-root users** for security
- **Minimal base images** to reduce attack surface
- **Explicit versioning** instead of `latest` tags

### Kubernetes Best Practices

- **Resource limits and requests** for proper scheduling
- **Health checks** for reliable deployments
- **Namespace isolation** for multi-tenancy
- **ConfigMaps and Secrets** for configuration management

### Production Recommendations

1. **Implement CI/CD pipeline** for automated deployments
2. **Add monitoring with Prometheus/Grafana**
3. **Set up centralized logging with Fluentd/ELK**
4. **Configure backup and disaster recovery**
5. **Implement GitOps with ArgoCD or Flux**

## 🚀 Future Enhancements

### Planned Improvements

- [ ] **Service Mesh**: Istio integration for advanced traffic management
- [ ] **GitOps**: ArgoCD for declarative deployments  
- [ ] **Observability**: Prometheus, Grafana, and Jaeger integration
- [ ] **Security**: Pod Security Standards and Network Policies
- [ ] **Multi-environment**: Development, staging, and production configs
- [ ] **Database Integration**: PostgreSQL deployment example

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Contribution Areas

- Documentation improvements
- Security enhancements
- Performance optimizations
- Additional deployment patterns
- Testing framework additions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Amazon EKS Team** for the excellent managed Kubernetes service
- **Kubernetes Community** for the robust orchestration platform
- **Flask Community** for the lightweight web framework
- **eksctl Contributors** for simplifying EKS cluster management

## 📞 Support

- **Documentation**: Check the `/docs` folder for detailed guides
- **Issues**: [GitHub Issues](https://github.com/ibraheemcisse/Python-Application-Deployment-on-Amazon-Elastic-Kubernetes-Service-EKS-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ibraheemcisse/Python-Application-Deployment-on-Amazon-Elastic-Kubernetes-Service-EKS-/discussions)

---

**⭐ If this project helps you learn Kubernetes and EKS, please give it a star! ⭐**
