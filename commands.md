# Cancer Agent - DevOps Commands Reference

This document serves as a cheat sheet for all the DevOps, Containerization, and Cloud Deployment commands used in this project.

---

## ☁️ How to Turn ON the Servers (AWS EKS)
*Run these commands whenever you want to boot up the production AWS cluster again. Everything is safely backed up, so it's a simple process.*

**1. Create the AWS EKS Cluster (Takes ~15-20 mins)**
```bash
eksctl create cluster --name onco-cluster --region us-east-1 --nodes 2 --node-type t3.medium
```

**2. Install AWS Storage Driver (Required for databases to run)**
```bash
eksctl utils associate-iam-oidc-provider --region=us-east-1 --cluster=onco-cluster --approve
eksctl create iamserviceaccount --name ebs-csi-controller-sa --namespace kube-system --cluster onco-cluster --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy --approve --role-only --role-name AmazonEKS_EBS_CSI_DriverRole
eksctl create addon --name aws-ebs-csi-driver --cluster onco-cluster --service-account-role-arn arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/AmazonEKS_EBS_CSI_DriverRole --force
```

**3. Deploy the Microservices**
```bash
kubectl apply -f kubernetes/
```

**4. Inject your secret OpenAI API Key** *(Replace YOUR_KEY with your actual key)*
```bash
kubectl set env deployment/agents-service OPENAI_API_KEY="sk-proj-YOUR_KEY"
kubectl set env deployment/rag-service OPENAI_API_KEY="sk-proj-YOUR_KEY"
```

**5. Get the Public URL**
```bash
kubectl get svc frontend
```
*(Copy the `EXTERNAL-IP` from the output, paste it into your browser, and add `:3000` to the end!)*

---

## 🛑 How to Turn OFF the Servers (Stop AWS Billing)
To completely delete the cluster, nodes, and load balancers to ensure you aren't charged a single cent while you are sleeping:
```bash
eksctl delete cluster --name onco-cluster --region us-east-1
```

---

## 🔄 Pushing Updates to AWS ECR
If you change any Next.js or Python code and want to upload the new versions to your AWS Cloud Registry:
```bash
# Make sure your AWS credentials are authenticated first
aws configure

# Run the automated deployment script
./push_to_ecr.sh
```

---

## 🐳 Docker & Minikube (Local Development)
If you want to test things locally without using AWS EKS.

**Start Docker Compose (Legacy Setup):**
```bash
docker compose up --build -d
```
**Stop Docker Compose:**
```bash
docker compose down -v
```

**Start Minikube (Local Kubernetes):**
```bash
minikube start --cpus=4 --memory=8192
```
**Point your terminal to Minikube's Docker Engine:**
```bash
eval $(minikube docker-env)
```
**Access the Frontend locally in Minikube:**
```bash
minikube service frontend
```
