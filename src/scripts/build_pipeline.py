# Contents of /InfraAuditAI/InfraAuditAI/src/scripts/build_pipeline.py

import os
import subprocess

def build_docker_image(image_name, dockerfile_path):
    """Builds a Docker image using the specified Dockerfile."""
    try:
        subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, "."], check=True)
        print(f"Docker image '{image_name}' built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building Docker image: {e}")

def main():
    """Main function to execute the build pipeline."""
    image_name = "infra_audit_ai:latest"
    dockerfile_path = os.path.join(os.path.dirname(__file__), "../../docker/Dockerfile")
    
    build_docker_image(image_name, dockerfile_path)

if __name__ == "__main__":
    main()