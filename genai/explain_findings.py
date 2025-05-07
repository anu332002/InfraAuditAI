import json
import os
from subprocess import run
import datetime

# Function to call a local AI model (like llama3 or mistral) using the `ollama` CLI tool.
# The function sends a prompt to the model and retrieves the response.
def call_ollama(prompt):
    """Call local ollama model like llama3 or mistral."""
    # Run the `ollama` command with the specified model and prompt.
    result = run(["ollama", "run", "llama3", prompt], capture_output=True, text=True)
    return result.stdout.strip()

# Function to load security findings from a JSON file.
def load_findings(file_path):
    """Load findings from a JSON file with encoding error handling."""
    try:
        # Try with utf-8 encoding first (most common for JSON)
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except UnicodeDecodeError:
        # If utf-8 fails, try with utf-8-sig (handles BOM)
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except UnicodeDecodeError:
            # Fallback to latin-1 which can read any byte value
            with open(file_path, "r", encoding="latin-1") as f:
                return json.load(f)

# Function to summarize and explain security findings using the AI model.
def summarize_findings(findings, source_type):
    """Summarize and explain the security findings."""
    explanation_prompt = f"Summarize and explain these {source_type} security findings in plain English:\n"
    explanation_prompt += json.dumps(findings, indent=2)
    return call_ollama(explanation_prompt)

# Function to save analysis to a log file
def save_to_log(content, log_file):
    """Save the analysis content to a log file with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    log_path = os.path.join('logs', log_file)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n\n=== Analysis completed at {timestamp} ===\n\n")
        f.write(content)
    
    print(f"Analysis saved to {log_path}")

# Main block of the script.
if __name__ == "__main__":
    # Process Checkov findings
    checkov_file = os.path.join('artifacts', 'checkov_report.json')
    trivy_file = os.path.join('artifacts', 'REPORT_TRIVY.json')
    
    print("\n=== AI Security Analysis ===\n")
    
    # Process Checkov findings first
    if os.path.exists(checkov_file):
        print("Processing Infrastructure as Code (Checkov) findings...")
        try:
            checkov_data = load_findings(checkov_file)
            
            # Extract failed checks from Checkov
            all_failed_checks = []
            for result in checkov_data:
                if isinstance(result, dict):
                    failed_checks = result.get("results", {}).get("failed_checks", [])
                    all_failed_checks.extend(failed_checks)
            
            if all_failed_checks:
                print("\n--- IaC Security Analysis ---")
                checkov_summary = summarize_findings(all_failed_checks[:3], "infrastructure code")
                print(checkov_summary)
                save_to_log(checkov_summary, 'checkov_analysis.log')
            else:
                message = "No infrastructure security issues found."
                print(message)
                save_to_log(message, 'checkov_analysis.log')
        except Exception as e:
            error_message = f"Error processing Checkov report: {str(e)}"
            print(error_message)
            save_to_log(error_message, 'checkov_analysis.log')
    
    # Process Trivy findings next
    if os.path.exists(trivy_file):
        print("\nProcessing Container Security (Trivy) findings...")
        try:
            trivy_data = load_findings(trivy_file)
            
            # Extract vulnerabilities from Trivy JSON
            vulnerabilities = []
            if "Results" in trivy_data:
                for result in trivy_data["Results"]:
                    if "Vulnerabilities" in result and result["Vulnerabilities"]:
                        # Take a subset of vulnerabilities for analysis
                        critical_high_vulns = [
                            v for v in result["Vulnerabilities"] 
                            if v.get("Severity") in ["CRITICAL", "HIGH"]
                        ][:3]  # Limit to 3 critical/high vulns
                        
                        if critical_high_vulns:
                            vulnerabilities.extend(critical_high_vulns)
            
            if vulnerabilities:
                print("\n--- Container Security Analysis ---")
                trivy_summary = summarize_findings(vulnerabilities, "container")
                print(trivy_summary)
                save_to_log(trivy_summary, 'trivy_analysis.log')
            else:
                message = "No significant container vulnerabilities found."
                print(message)
                save_to_log(message, 'trivy_analysis.log')
        except Exception as e:
            error_message = f"Error processing Trivy report: {str(e)}"
            print(error_message)
            save_to_log(error_message, 'trivy_analysis.log')
    else:
        print("\nTrivy scan report not found.")
    
    # If neither report is found
    if not os.path.exists(checkov_file) and not os.path.exists(trivy_file):
        print("No security scan reports found.")