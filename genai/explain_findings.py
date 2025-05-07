import json
import os
from subprocess import run

# Function to call a local AI model (like llama3 or mistral) using the `ollama` CLI tool.
# The function sends a prompt to the model and retrieves the response.
def call_ollama(prompt):
    """Call local ollama model like llama3 or mistral."""
    # Run the `ollama` command with the specified model and prompt.
    result = run(["ollama", "run", "llama3", prompt], capture_output=True, text=True)
    return result.stdout.strip()

# Function to load security findings from a JSON file.
def load_findings(file_path):
    """Load the Checkov findings from a JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)

# Function to summarize and explain security findings using the AI model.
def summarize_findings(findings):
    """Summarize and explain the security findings."""
    explanation_prompt = "Summarize and explain these security findings in plain English:\n"
    explanation_prompt += json.dumps(findings[:3], indent=2)  # Limit for brevity
    return call_ollama(explanation_prompt)

# Main block of the script.
if __name__ == "__main__":
    file = os.path.join('artifacts', 'checkov_report.json')
    
    if os.path.exists(file):
        findings = load_findings(file)
        
        # NEW: Iterate through the findings list and collect all failed checks
        all_failed_checks = []
        for result in findings:
            if isinstance(result, dict):  # Make sure it's a dictionary before accessing keys
                failed_checks = result.get("results", {}).get("failed_checks", [])
                all_failed_checks.extend(failed_checks)

        # Generate the explanation for the failed checks
        summary = summarize_findings(all_failed_checks)
        print("\nAI Explanation of Findings:\n", summary)
    else:
        print("Scan report not found.")
