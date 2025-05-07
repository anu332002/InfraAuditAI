# Architecture Overview

## Introduction

The architecture of the InfraAuditAI project is designed to facilitate a robust, scalable, and automated DevOps pipeline. This document outlines the key components, their interactions, and the overall structure of the system.

## System Components

1. **Source Code Repository**
   - The application code is hosted in a Git repository, which triggers the CI/CD pipeline upon code commits.

2. **CI/CD Pipeline**
   - **Jenkins**: The Jenkins server orchestrates the CI/CD process, automating the build, test, and deployment stages.
   - **Jenkinsfile**: Defines the stages and steps for the CI/CD pipeline, including building the application, running tests, and deploying to the Kubernetes cluster.

3. **Containerization**
   - **Docker**: The application is containerized using Docker, ensuring consistency across different environments. The Dockerfile specifies the base image, dependencies, and commands to run the application.
   - **Docker Compose**: Used for defining and running multi-container Docker applications.

4. **Kubernetes Orchestration**
   - The application is deployed on a Kubernetes cluster, which manages the deployment, scaling, and operation of the application containers.
   - **Kubernetes Manifests**: Deployment and service configurations are defined in YAML files, allowing for easy updates and management of application instances.

5. **Monitoring and Logging**
   - **Prometheus**: Monitors application and infrastructure metrics, providing insights into system performance.
   - **Grafana**: Visualizes metrics collected by Prometheus, allowing for real-time monitoring and alerting.
   - **ELK Stack**: Collects and analyzes logs from the application and infrastructure, providing a centralized logging solution.

6. **Artifact Management**
   - **JFrog Artifactory**: Stores build artifacts and Docker images, ensuring version control and consistency across deployments.

7. **Security Scanning**
   - **Scanner**: Implements scanning logic to check for vulnerabilities or compliance issues in the application code and infrastructure as code.
   - **Checkov**: A static code analysis tool used to scan infrastructure as code, with configurations defined in a YAML file.

8. **Reporting**
   - Scan results are stored in JSON format, providing insights into vulnerabilities or issues found during the scanning process.

## Conclusion

The InfraAuditAI architecture leverages modern DevOps practices and tools to create a streamlined, automated delivery process. By integrating CI/CD, containerization, orchestration, monitoring, and security scanning, the project aims to reduce deployment time and failures, ultimately improving reliability and developer productivity.