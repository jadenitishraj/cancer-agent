#!/bin/bash

# Ensure AWS CLI is configured
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "❌ AWS CLI is not configured or credentials are invalid. Please run 'aws configure' first."
    exit 1
fi

REGION=$(aws configure get region)
if [ -z "$REGION" ]; then
    echo "❌ AWS region is not set. Please run 'aws configure' and set a default region."
    exit 1
fi

REGISTRY_URL="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
echo "🔐 Authenticating Docker to ECR at ${REGISTRY_URL}..."
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${REGISTRY_URL}

# Point Docker to the Minikube daemon (where our images were built)
echo "🐳 Pointing Docker to Minikube environment..."
eval $(minikube docker-env)

# Define the images we want to push
IMAGES=(
    "cancer-agent-agents-service"
    "cancer-agent-backend-gateway"
    "cancer-agent-frontend"
    "cancer-agent-langraph-orchestrator"
    "cancer-agent-rag-service"
    "cancer-agent-tools-service"
)

for IMAGE in "${IMAGES[@]}"; do
    echo "----------------------------------------"
    echo "📦 Processing ${IMAGE}..."
    
    # Check if repository exists, create if it doesn't
    aws ecr describe-repositories --repository-names "${IMAGE}" --region "${REGION}" >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "   Creating ECR repository ${IMAGE}..."
        aws ecr create-repository --repository-name "${IMAGE}" --region "${REGION}" >/dev/null
    else
        echo "   ECR repository ${IMAGE} already exists."
    fi

    # Tag the local image for ECR
    echo "   Tagging image..."
    docker tag "${IMAGE}:latest" "${REGISTRY_URL}/${IMAGE}:latest"

    # Push to ECR
    echo "   Pushing to ECR..."
    docker push "${REGISTRY_URL}/${IMAGE}:latest"
    
    echo "✅ Successfully pushed ${IMAGE}"
done

echo "🎉 All images have been pushed to ECR!"
