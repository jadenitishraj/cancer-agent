# Task Plan: GitHub Actions EKS Deployment

- **Status**: `[Completed]`
- **Date**: 2026-06-21
- **Author**: Antigravity

## 📋 To-Do List
- [x] **Task Planning**: Create task plan and submit for approval
- [x] **Kubernetes Manifest Updates**: Secure OpenAI API key env variables by pulling from Kubernetes secrets
- [x] **GitHub Actions Workflow**: Create deploy.yml to build, push to ECR, and deploy to EKS
- [x] **Verification**: Validate file structures and push files for run

---

## 1. Objective & Requirements
Create a CI/CD pipeline using GitHub Actions that triggers when changes are pushed to the `main` branch.
The workflow needs to:
1. Authenticate with AWS.
2. Build and tag Docker images for frontend, backend-gateway, tools-service, agents-service, langraph-orchestrator, and rag-service.
3. Push the images to Amazon ECR.
4. Update the Kubernetes deployment manifests with the specific commit SHA to ensure rolling updates.
5. Deploy/apply the updated manifests to the AWS EKS cluster.

Additionally, update manifests to retrieve the OpenAI API Key from a secure Secret `openai-secret` instead of using a hardcoded dummy value.

---

## 2. Proposed Changes

### 📂 Files to Create / Modify
- [x] `kubernetes/agents-service-deployment.yaml` – Modify OPENAI_API_KEY to retrieve from a secret key reference.
- [x] `kubernetes/rag-service-deployment.yaml` – Modify OPENAI_API_KEY to retrieve from a secret key reference.
- [x] `.github/workflows/deploy.yml` – [NEW] Create GitHub Actions workflow file.

---

## 3. Verification & Testing Plan
- Validate yaml files format.
- User pushes code to trigger and verify the GitHub Actions workflow in their repository.

---

## 4. User Sign-Off
- [x] **User Approval**: Approved by user on 2026-06-21
