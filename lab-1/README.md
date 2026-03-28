# Lab 1

## Scenario & Lab Description
The development team has handed over the source code for a lightweight Python backend API. Currently, this application only runs on developers' local machines. Your objective is to containerize this application, distribute it via a container registry, and deploy the first iteration to a development Kubernetes cluster.

## Detailed Tasks

### 1. Containerization
Write a Dockerfile that packages the Python application. Ensure the image is optimized (e.g., using a lightweight base image) and runs securely as a non-root user.

### 2. Registry Distribution
Build the Docker image and push it to a public repository on DockerHub.

### 3. Basic Deployment
Create a Kubernetes Deployment manifest that pulls your image from DockerHub and runs a single replica.

### 4. Internal Access
Create a Service manifest (ClusterIP) to expose the application internally within the cluster on port 8080.

### 5. The Blocker (Troubleshooting)
Once applied, the Pod will enter a `CrashLoopBackOff` state. You must inspect the Pod logs to discover that the application explicitly requires an environment variable named `FLASK_ENV` to initialize. You must troubleshoot and update your manifests to resolve this crash without modifying the application source code.