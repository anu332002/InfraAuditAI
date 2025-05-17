# InfraAuditAI

## Project Demo: [InfraAuditAI Demo](https://drive.google.com/file/d/17pE1CITLk2yjzuRhPJz3ED4VchD_gN5R/view)
## Business Problem

Many organizations suffer from slow, error-prone releases and unplanned downtime due to manual build and deployment processes. Uncoordinated environments and hand-crafted deployments lead to failed releases and costly outages. For example, research estimates unplanned IT downtime costs about **$5,600 per minute**. Manually handling code builds, environment configuration, and deployments makes teams firefight issues instead of innovating. The business problem is to reduce deployment time and failures by adopting a reproducible, automated delivery process.

## DevOps Solution Approach

A DevOps approach solves this by **automating the build-test-deploy pipeline**, containerizing applications for consistency, and orchestrating them at scale. Key components and tools include:

* **Jenkins (CI/CD):** Automates building, testing, and deploying code. Jenkins is a mature, extensible automation server used worldwide for CI/CD. It can serve as the “delivery hub” that triggers pipelines on code commits.
* **Docker Containers:** Package the application and its dependencies into a standardized, portable image. Docker ensures the app runs the same in development, testing, and production.
* **Kubernetes:** An open-source system to orchestrate containers across clusters. Kubernetes automates deployment, scaling, and management of containerized services, letting the app scale to meet demand.
* **Python Scripting:** Python is widely used in DevOps for automation. It is known for readability and rich libraries, with about 26% of Python usage in DevOps/automation tasks. Python scripts can automate tests, environment setup, or invoke APIs in the pipeline.
* **Artifact Repository (JFrog Artifactory):** Stores and manages build artifacts and Docker images. Artifactory provides a central, versioned “single source of truth” for binaries and container images. This ensures teams use approved, consistent artifact versions in deployments.
* **Monitoring & Logging:** Open-source tools like **Prometheus** (for metrics) and **Grafana** (for dashboards) are used for monitoring. Prometheus is a CNCF project (fully open-source) that collects time-series metrics. For logging, an ELK stack (Elasticsearch, Fluentd/Logstash, Kibana) can aggregate logs and provide alerts. These tools ensure visibility into system health and quick detection of issues.

## Proposed Project Idea

**Project:** Build a sample cloud-native web application (e.g. a simple e-commerce API) to demonstrate a full DevOps pipeline. The project will implement:

1. **Git Code Repository:** Host the application code (e.g. on GitHub). Configure a webhook so pushes trigger the pipeline.
2. **Jenkins Pipeline:** On each code push, Jenkins (running on a Linux VM or container) pulls the code, runs unit tests (using Python test scripts), and builds a Docker image if tests pass.
3. **Docker Build & Artifactory:** Jenkins builds a Docker image and pushes it to JFrog Artifactory (or an equivalent Docker registry). Artifactory manages image versions for the project.
4. **Kubernetes Deployment:** A Kubernetes cluster (e.g. on AWS EKS or GCP GKE, or on-prem) is configured with Deployment and Service manifests. Jenkins (via kubectl or Helm) applies these manifests to update the running pods to the new image. Kubernetes performs rolling updates to avoid downtime.
5. **Automated Testing:** After deployment, Jenkins or separate jobs run integration tests (e.g. Python scripts hitting the API) to verify functionality in the cluster.
6. **Monitoring and Logging:** Prometheus (running in-cluster) scrapes application and cluster metrics, Grafana dashboards visualize them, and alert rules notify on anomalies. Logs from the app and infrastructure are collected in Elasticsearch and visualized in Kibana.

This pipeline ensures that every code change is automatically built, tested, and deployed to a scalable environment. Automation eliminates manual errors and drastically reduces time-to-market, addressing the initial business problem of slow, unreliable deployments.

## Architecture and Components

*Figure: Example of a server infrastructure (data center) that hosts the CI/CD pipeline and Kubernetes cluster.* The system architecture has the following components. **Jenkins** (hosted on a VM or container, on-prem or cloud) orchestrates the CI/CD pipeline. Developers commit code, Jenkins runs automated **Python scripts** for testing and builds Docker images. Built images and binaries are stored in **JFrog Artifactory** (or an equivalent registry) as a central artifact repository. A **Kubernetes cluster** (e.g. AWS EKS or on-prem) pulls the approved images from Artifactory and runs them as pods behind a Service. **Prometheus** monitors application and cluster metrics, feeding Grafana dashboards. **Logging** agents ship logs to an ELK stack for centralized search/alerts. All infrastructure (CI server, artifact repo, Kubernetes nodes) runs on alternative platforms (such as AWS, GCP, or on-premises servers).

* **Jenkins Server:** Deployed on an EC2 or on-prem Linux VM. It uses pipeline scripts to connect to Git, run builds, and trigger deployments.
* **Artifact Repository:** JFrog Artifactory (or Nexus) stores Docker images and build artifacts. It provides version control for binaries and packages.
* **Container Registry:** Docker images are tagged (e.g. v1.0.0) and pushed to Artifactory. Teams can roll back by pulling previous versions.
* **Kubernetes Cluster:** A multi-node K8s cluster (AWS EKS / GCP GKE or on-prem) that automatically schedules and scales application containers. Kubernetes manages config (via ConfigMaps/Secrets) so environments remain consistent.
* **Monitoring/Logging:** Prometheus (CNCF project) runs in-cluster to scrape metrics. Grafana provides visual dashboards. The ELK (Elasticsearch + Kibana) stack collects logs. Alerts (via Prometheus Alertmanager or Kibana) notify the team of failures or threshold breaches.

## Platform Alternatives

This solution avoids Azure by using alternative cloud or on-prem platforms:

* **AWS:** Use EC2 instances for Jenkins and Artifactory, and Amazon EKS for Kubernetes. Docker images could also be stored in AWS ECR (as a simpler alternative). CloudWatch can complement Prometheus for AWS-native logging/metrics.
* **GCP:** Use Google Compute Engine for Jenkins/Artifactory, and GKE for the K8s cluster. Google Container Registry (GCR) can host images. Stackdriver (Cloud Logging/Monitoring) can be used alongside Prometheus.
* **On-Premises:** Deploy Jenkins, Artifactory, and Kubernetes on local servers or VMs. Use a private Docker registry (Artifactory) and tools like Prometheus/Grafana and ELK on-prem. Infrastructure as Code (e.g. Terraform) can provision on-prem resources.

Each alternative provides the same core components (Jenkins, Docker, K8s, etc.) but with different hosting: AWS/GCP for cloud or bare-metal servers for on-prem. This flexibility shows the solution’s portability, as Kubernetes and containers are cloud-agnostic.

## Conclusion

By implementing this DevOps pipeline, the team transforms manual, error-prone processes into an automated, continuous workflow. Jenkins automates builds/tests, Docker ensures consistency, and Kubernetes provides scalable deployment. Python scripts tie together CI tasks, while Artifactory securely manages binaries. Monitoring with Prometheus/Grafana adds visibility into performance. This comprehensive solution addresses the business problem by drastically reducing deployment time and failures, improving reliability and developer productivity. It would make an excellent portfolio project for a DevOps engineer.
