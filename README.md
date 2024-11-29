# ben
# Microservices Application with Kubernetes and Docker

## Overview
This repository contains a microservices-based application with the following services:
1. **User Authentication Service** - Handles user signup and authentication.
2. **Quest Catalog Service** - Manages available quests and rewards.
3. **Quest Processing Service** - Tracks user progress and quest completion.

### Key Features:
- Microservices architecture with **FastAPI**.
- Deployment using **Docker** and **Kubernetes**.
- Load balancing via **Kubernetes Ingress**.
- Caching strategies for scalability.
- Supports horizontal scaling for API Gateway and services.

---

## **Setup and Deployment Guide**

### Prerequisites
1. **Docker** installed ([Download here](https://www.docker.com/products/docker-desktop)).
2. **Kubectl** CLI ([Install Guide](https://kubernetes.io/docs/tasks/tools/)).
3. A Kubernetes cluster (use Docker Desktop Kubernetes or [Minikube](https://minikube.sigs.k8s.io/docs/start/)).
4. Git CLI ([Install Guide](https://git-scm.com/)).

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/RumbleInCybertron/ben.git
cd ben/backend
```

### Step 2: Build Docker Images

Navigate to the root directory and build the Docker images:
```bash
docker build -t user-auth-service ./user_auth_service
docker build -t quest-catalog-service ./quest_catalog_service
docker build -t quest-processing-service ./quest_processing_service
docker build -t api-gateway ./api_gateway
```

Push the images to a container registry (e.g., Docker Hub):
```bash
docker tag user-auth-service:latest your-docker-username/user-auth-service:latest
docker push your-docker-username/user-auth-service:latest
docker tag user-auth-service:latest your-docker-username/quest-catalog-service:latest
docker push your-docker-username/quest-catalog-service:latest
docker tag user-auth-service:latest your-docker-username/quest-processing-service:latest
docker push your-docker-username/quest-processing-service:latest
docker tag user-auth-service:latest your-docker-username/api-gateway:latest
docker push your-docker-username/api-gateway:latest
```

### Step 3: Deploy Kubernetes Resources
Apply the Kubernetes configurations:
```bash
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/user-auth-db-deployment.yml
kubectl apply -f k8s/user-auth-db-service.yml
kubectl apply -f k8s/quest-catalog-db-deployment.yml
kubectl apply -f k8s/quest-catalog-db-service.yml
kubectl apply -f k8s/quest-processing-db-deployment.yml
kubectl apply -f k8s/quest-processing-db-service.yml
kubectl apply -f k8s/user-auth-service-deployment.yml
kubectl apply -f k8s/user-auth-service.yml
kubectl apply -f k8s/quest-catalog-service-deployment.yml
kubectl apply -f k8s/quest-catalog-service.yml
kubectl apply -f k8s/quest-processing-service-deployment.yml
kubectl apply -f k8s/quest-processing-service.yml
kubectl apply -f k8s/api-gateway-deployment.yml
kubectl apply -f k8s/api-gateway-service.yml
kubectl apply -f k8s/ingress.yml
```

### Step 4: Access the Application

1.  Find the Ingress IP:
```bash
kubectl get ingress -n app-namespace
```
Use the external IP to access the application:

  *  API Gateway: `http://localhost/` (via Kubernetes Ingress).

If Kubernetes Ingress is not set up, you can expose the API Gateway service directly using port forwarding:

```bash
kubectl port-forward service/api-gateway 8000:8000 -n app-namespace
```

This will make the API Gateway accessible at `http://localhost:8000`.

### Step 5: Scaling the Services

Scale a service using `kubectl scale`:
```bash
kubectl scale deployment api-gateway --replicas=3 -n app-namespace
kubectl scale deployment user-auth-service --replicas=3 -n app-namespace
```