# Helm Quick Start for Atlas4D Base

Deploy Atlas4D Base to Kubernetes with Helm.

## Prerequisites

- Kubernetes cluster (kind, minikube, or cloud)
- Helm 3.x installed
- kubectl configured

## Quick Start (Local with kind)

### 1. Create a local cluster
```bash
# Install kind if needed
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Create cluster
kind create cluster --name atlas4d
```

### 2. Install Atlas4D Base
```bash
# Clone the repository
git clone https://github.com/crisbez/atlas4d-base.git
cd atlas4d-base

# Install with Helm
helm install atlas4d ./deploy/helm/atlas4d-base

# Check status
kubectl get pods -w
```

### 3. Access the services
```bash
# Port-forward frontend
kubectl port-forward svc/atlas4d-frontend 8091:80 &

# Port-forward API gateway
kubectl port-forward svc/atlas4d-gateway 8090:8090 &

# Open in browser
echo "Frontend: http://localhost:8091"
echo "API: http://localhost:8090/health"
```

## Configuration

### Custom values

Create a `my-values.yaml`:
```yaml
postgres:
  auth:
    password: "my-secure-password"
  persistence:
    size: 20Gi

frontend:
  service:
    type: NodePort
    nodePort: 30091
```

Install with custom values:
```bash
helm install atlas4d ./deploy/helm/atlas4d-base -f my-values.yaml
```

### Common overrides
```bash
# Disable persistence (for testing)
helm install atlas4d ./deploy/helm/atlas4d-base \
  --set postgres.persistence.enabled=false

# Use NodePort instead of LoadBalancer
helm install atlas4d ./deploy/helm/atlas4d-base \
  --set frontend.service.type=NodePort

# Custom password
helm install atlas4d ./deploy/helm/atlas4d-base \
  --set postgres.auth.password="$(openssl rand -base64 32)"
```

## Verify Installation
```bash
# Check all pods are running
kubectl get pods

# Expected output:
# NAME                               READY   STATUS    RESTARTS   AGE
# atlas4d-frontend-xxx               1/1     Running   0          1m
# atlas4d-gateway-xxx                1/1     Running   0          1m
# atlas4d-postgres-xxx               1/1     Running   0          1m
# atlas4d-redis-xxx                  1/1     Running   0          1m

# Check services
kubectl get svc

# Test health endpoint
kubectl port-forward svc/atlas4d-gateway 8090:8090 &
curl http://localhost:8090/health
```

## Uninstall
```bash
helm uninstall atlas4d

# Delete PVC if needed
kubectl delete pvc atlas4d-postgres-pvc
```

## Minikube Alternative
```bash
# Start minikube
minikube start --memory=4096 --cpus=2

# Install
helm install atlas4d ./deploy/helm/atlas4d-base \
  --set frontend.service.type=NodePort

# Get URL
minikube service atlas4d-frontend --url
```

## Production Considerations

1. **Use secrets management** - Don't commit passwords
2. **Enable persistence** - Use proper StorageClass
3. **Configure resources** - Adjust based on load
4. **Use Ingress** - For proper domain routing
5. **Enable TLS** - Use cert-manager

## Troubleshooting
```bash
# Check pod logs
kubectl logs -l app=atlas4d-gateway

# Describe failing pod
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

## Next Steps

- Configure [Ingress](../architecture/NETWORKING.md)
- Set up [Monitoring](../observability/GRAFANA.md)
- Load [Demo Data](../quickstart/QUICK_START.md)
