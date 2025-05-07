# Contents of /InfraAuditAI/InfraAuditAI/src/scripts/deploy_pipeline.py

import os
import subprocess

def deploy_application():
    """
    Deploy the application to the Kubernetes cluster.
    This function assumes that the Kubernetes context is set correctly.
    """
    try:
        # Apply the Kubernetes deployment and service manifests
        subprocess.run(["kubectl", "apply", "-f", "../configs/kubernetes/deployment.yaml"], check=True)
        subprocess.run(["kubectl", "apply", "-f", "../configs/kubernetes/service.yaml"], check=True)
        
        print("Deployment successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during deployment: {e}")
        raise

if __name__ == "__main__":
    deploy_application()