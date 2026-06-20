# AWS EKS Deployment & Networking Plan

## 1. Networking Architecture & URL Management (The Proxy Pattern)
Currently, the user's browser attempts to talk directly to the Backend Gateway. In AWS EKS, exposing multiple LoadBalancers and handling CORS is inefficient and insecure.

**The Solution:**
1. **Frontend Proxy:** We will modify the Next.js frontend to send requests to its own relative URL (e.g., `fetch('/api/chat')`).
2. **Next.js Server Route:** We will create a Next.js server-side API route (`src/app/api/chat/route.ts`). When the browser calls this route, the Next.js server will forward the request to the Backend Gateway using the secure, internal Kubernetes DNS (`http://backend-gateway:8000/api/chat`).
3. **Internal API Links:** All backend services (Agents, Orchestrator, Chroma, RAG, Tools) will continue to use their internal Kubernetes Service names (`http://rag-service:8004`, etc.). These do not need to change for EKS.

## 2. Code Updates Required
- Update `frontend/src/app/page.tsx` to call `/api/chat` instead of `http://127.0.0.1:8000/api/chat`.
- Create the proxy route in the frontend.
- Rebuild the frontend Docker image and push the updated image to ECR.

## 3. Kubernetes Manifest Updates
To run on EKS, we must update the YAML manifests:
- **Images:** Update the `image:` fields in all deployments to point to your new AWS ECR URIs (e.g., `455254973218.dkr.ecr.us-east-1.amazonaws.com/cancer-agent-frontend:latest`).
- **Load Balancer:** Change the `frontend-service.yaml` to `type: LoadBalancer`. This tells AWS to automatically provision an Elastic Load Balancer (ELB) and give us a public URL to access the site.

## 4. EKS Infrastructure Provisioning
1. Install `eksctl` (the official CLI for Amazon EKS).
2. Create the EKS cluster using `eksctl create cluster --name onco-cluster --region us-east-1 --nodes 2 --node-type t3.medium`.
3. Update local `kubeconfig` to point `kubectl` to the new AWS cluster instead of Minikube.

## 5. Deployment & Verification
- Apply the updated manifests: `kubectl apply -f kubernetes/`.
- Fetch the public AWS Load Balancer URL: `kubectl get svc frontend`.
- Open the URL in the browser and test the RAG multi-agent system.
