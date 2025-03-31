#!/bin/bash

# Build images
docker build -t sample-app:latest ./app
docker build -t scaling-predictor:latest ./ml-predictor

# Load images to Minikube
minikube image load sample-app:latest
minikube image load scaling-predictor:latest

# Deploy base components
kubectl apply -f k8s/01-namespace.yaml
kubectl apply -f k8s/07-rbac.yaml

# Deploy monitoring
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl apply -f k8s/05-prometheus.yaml
kubectl apply -f k8s/06-grafana.yaml

# Deploy application
kubectl apply -f k8s/02-deployment.yaml
kubectl apply -f k8s/03-service.yaml
kubectl apply -f k8s/04-hpa.yaml
kubectl apply -f k8s/08-metrics-adapter.yaml

echo "Deployment complete!"
echo "Access dashboard with: minikube service grafana -n autoscale-system"