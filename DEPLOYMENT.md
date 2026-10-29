# 🚀 Deployment Guide

Complete guide for deploying the Insurance Claim Processing System to production.

## Local Development

### Setup

```bash
# Clone repository
git clone <repo-url>
cd insurance-claim-processor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Initialize
python setup.py

# Run
streamlit run ui/app.py
```

### Development Server

```bash
# Start with auto-reload
streamlit run ui/app.py --logger.level=debug

# Custom port
streamlit run ui/app.py --server.port 8502

# Remote access
streamlit run ui/app.py --server.address 0.0.0.0
```

---

## Docker Deployment

### Single Container

#### Build
```bash
docker build -t insurance-processor:latest .
```

#### Run
```bash
docker run -d \
  --name insurance-processor \
  -p 8501:8501 \
  -e AZURE_OPENAI_API_KEY=<key> \
  -e AZURE_OPENAI_ENDPOINT=<endpoint> \
  -e OPENAI_API_KEY=<key> \
  -v /data:/app/data \
  -v /logs:/app/logs \
  insurance-processor:latest
```

#### Logs
```bash
docker logs -f insurance-processor
```

### Docker Compose

#### Setup
```bash
# Create .env file with your keys
cp .env.example .env

# Edit .env
nano .env
```

#### Deploy
```bash
# Start
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

#### Scale
```bash
docker-compose up -d --scale insurance-claim-processor=3
```

---

## Cloud Deployment

### Azure Container Instances (ACI)

#### Prerequisites
```bash
az login
az account set --subscription <subscription-id>
```

#### Deploy
```bash
# Create resource group
az group create --name insurance-rg --location eastus

# Build and push image
az acr build --registry <acr-name> --image insurance-processor:latest .

# Deploy container
az container create \
  --resource-group insurance-rg \
  --name insurance-processor \
  --image <acr-name>.azurecr.io/insurance-processor:latest \
  --ports 8501 \
  --environment-variables \
    AZURE_OPENAI_API_KEY=<key> \
    AZURE_OPENAI_ENDPOINT=<endpoint> \
  --cpu 2 \
  --memory 4 \
  --registry-login-server <acr-name>.azurecr.io \
  --registry-username <username> \
  --registry-password <password>
```

#### Access
```bash
# Get URL
az container show --resource-group insurance-rg --name insurance-processor --query ipAddress.fqdn
```

### AWS ECS

#### Prerequisites
```bash
aws configure
```

#### Create Task Definition
```bash
# Create task-definition.json
cat > task-definition.json << EOF
{
  "family": "insurance-processor",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "insurance-processor",
      "image": "<account>.dkr.ecr.<region>.amazonaws.com/insurance-processor:latest",
      "portMappings": [{"containerPort": 8501}],
      "environment": [
        {"name": "AZURE_OPENAI_API_KEY", "value": "<key>"},
        {"name": "AZURE_OPENAI_ENDPOINT", "value": "<endpoint>"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/insurance-processor",
          "awslogs-region": "<region>",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

# Register
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### Deploy
```bash
# Create cluster
aws ecs create-cluster --cluster-name insurance

# Run task
aws ecs run-task \
  --cluster insurance \
  --task-definition insurance-processor \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}"
```

### Google Cloud Run

#### Deploy
```bash
# Configure
gcloud config set project <project-id>

# Build
gcloud builds submit --tag gcr.io/<project-id>/insurance-processor

# Deploy
gcloud run deploy insurance-processor \
  --image gcr.io/<project-id>/insurance-processor \
  --port 8501 \
  --memory 2Gi \
  --cpu 1 \
  --timeout 3600 \
  --allow-unauthenticated \
  --set-env-vars AZURE_OPENAI_API_KEY=<key>,AZURE_OPENAI_ENDPOINT=<endpoint>
```

---

## Kubernetes Deployment

### Prerequisites
```bash
kubectl cluster-info
```

### Create Deployment Manifest

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: insurance-processor
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: insurance-processor
  template:
    metadata:
      labels:
        app: insurance-processor
    spec:
      containers:
      - name: insurance-processor
        image: insurance-processor:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8501
        env:
        - name: AZURE_OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        - name: AZURE_OPENAI_ENDPOINT
          value: "https://xxx.openai.azure.com/"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 10
          periodSeconds: 5
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: insurance-data
      - name: logs
        persistentVolumeClaim:
          claimName: insurance-logs
---
apiVersion: v1
kind: Service
metadata:
  name: insurance-processor-service
spec:
  selector:
    app: insurance-processor
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

### Deploy
```bash
# Create secrets
kubectl create secret generic openai-secret --from-literal=api-key=<key>

# Create PVCs
kubectl apply -f - << EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: insurance-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: insurance-logs
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
EOF

# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl get deployments
kubectl get pods
kubectl get svc
```

---

## Production Configuration

### Environment Variables

```env
# LLM Configuration
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large

# Fallback OpenAI
OPENAI_API_KEY=sk-<your-key>

# Vector Store
CHROMA_DB_PATH=/data/chroma_db
CHROMA_COLLECTION_NAME=insurance_claims

# Application
LOG_LEVEL=INFO
DEBUG=False
GUARDRAILS_ENABLED=True

# Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=True
STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
```

### Security Best Practices

1. **API Keys**
   ```bash
   # Use secrets management
   # Never commit .env file
   # Rotate keys regularly
   # Use environment variables in production
   ```

2. **Network**
   ```bash
   # Use HTTPS only
   # Enable authentication
   # Restrict access by IP
   # Use VPN/bastion hosts
   ```

3. **Data Protection**
   ```bash
   # Enable encryption at rest
   # Use encrypted volumes
   # Enable audit logging
   # Regular backups
   ```

4. **Monitoring**
   ```bash
   # Monitor memory usage
   # Track API call counts
   # Alert on errors
   # Monitor response times
   ```

---

## Monitoring & Logging

### Log Aggregation

#### Using ELK Stack
```bash
# Elasticsearch, Logstash, Kibana
docker-compose up -d elasticsearch logstash kibana

# Configure Logstash to read app logs
# Visualize in Kibana at http://localhost:5601
```

#### Using CloudWatch (AWS)
```bash
# Already configured in task definition
# View logs:
aws logs tail /ecs/insurance-processor --follow
```

#### Using Azure Monitor
```bash
# Configure application insights
pip install azure-monitor-opentelemetry
```

### Performance Monitoring

```bash
# Monitor resource usage
docker stats insurance-processor

# Check response times
curl -w "@curl-format.txt" http://localhost:8501

# Load testing
siege -c 10 -r 10 http://localhost:8501
```

---

## Backup & Recovery

### Backup Vector Store
```bash
# Backup ChromaDB
tar -czf chroma_backup.tar.gz data/chroma_db/

# Restore
tar -xzf chroma_backup.tar.gz
```

### Backup Configuration
```bash
# Store .env securely
# Use secrets manager (AWS Secrets Manager, Azure Key Vault)
# Never commit to version control
```

### Restore Procedure
```bash
# 1. Deploy container
# 2. Restore data volume
# 3. Restore .env secrets
# 4. Run setup.py
# 5. Verify health checks
```

---

## Auto-Scaling

### Docker Swarm
```bash
# Initialize
docker swarm init

# Deploy service with auto-scaling
docker service create \
  --name insurance-processor \
  --replicas 3 \
  -p 8501:8501 \
  --env AZURE_OPENAI_API_KEY=<key> \
  insurance-processor:latest
```

### Kubernetes Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: insurance-processor-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: insurance-processor
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs insurance-processor

# Verify image
docker images

# Check resources
docker stats
```

### High memory usage
```bash
# Clear ChromaDB cache
docker exec insurance-processor rm -rf data/chroma_db

# Reduce batch size
# Set RAGAS_BATCH_SIZE=5 in .env
```

### Slow response times
```bash
# Check LLM API rate limits
# Increase timeouts
# Add caching layer (Redis)
# Optimize retrieval (reduce k)
```

### PII detection failing
```bash
# Verify Presidio is installed
pip install presidio-analyzer presidio-anonymizer

# Check language setting (should be 'en')
# Verify spacy model is downloaded
```

---

## Performance Tuning

### For High Throughput
```env
RAGAS_BATCH_SIZE=20
LOG_LEVEL=WARNING
STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
```

### For Low Latency
```env
CHROMA_DB_PATH=/ssd/chroma_db  # Use fast storage
RAGAS_BATCH_SIZE=1
STREAMLIT_CLIENT_SHOW_ERRORS_IN_SIDEBAR=False
```

### For Cost Optimization
```env
# Use gpt-3.5-turbo (not gpt-4)
# Limit max_tokens
# Cache LLM responses
# Use smaller embedding model
```

---

## Health Checks

### Endpoint
```bash
curl http://localhost:8501/_stcore/health
```

### Docker Health Check
```bash
docker ps --filter name=insurance-processor --format "table {{.Names}}\t{{.Status}}"
```

### Kubernetes Probe
```yaml
livenessProbe:
  httpGet:
    path: /_stcore/health
    port: 8501
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

## Post-Deployment

1. **Verify Health**
   ```bash
   curl http://<your-domain>/_stcore/health
   ```

2. **Test Processing**
   - Submit a test claim
   - Verify decision output
   - Check logs

3. **Monitor Resources**
   - CPU usage
   - Memory usage
   - API call counts
   - Response times

4. **Setup Alerts**
   - High CPU/memory
   - API errors
   - Response time SLOs

---

## Support

For deployment issues:
1. Check logs: `docker logs`
2. Review README.md
3. Consult ARCHITECTURE.md
4. Run test_system.py

Happy deploying! 🚀
