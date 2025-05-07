import json
import os
from subprocess import run

def call_ollama(prompt):
    """
    Call local ollama model (like llama3 or mistral) with the given prompt.
    Returns the model's response as a string.
    """
    try:
        result = run(["ollama", "run", "llama3", prompt], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"[Error calling Ollama]: {str(e)}"

def load_findings(file_path):
    """
    Load findings from a given JSON file path.
    Returns the parsed JSON object.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error loading file {file_path}]: {e}")
        return {}

def summarize_findings(findings, tool_name):
    """
    Prepare a prompt to summarize and explain findings using the AI model.
    """
    if not findings:
        return f"No findings to summarize for {tool_name}."

    explanation_prompt = f"Summarize and explain these {tool_name} security findings in plain English:\n"
    explanation_prompt += json.dumps(findings[:3], indent=2)  # limit to 3 findings
    return call_ollama(explanation_prompt)

def explain_and_log(findings, tool_name):
    """
    Generate AI explanation and write to logs/ai_explanation.log.
    """
    explanation = summarize_findings(findings, tool_name)

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    with open("logs/ai_explanation.log", "a") as log_file:
        log_file.write(f"\n=== {tool_name} Findings ===\n")
        log_file.write(explanation + "\n")

if __name__ == "__main__":
    checkov_file = "artifacts/checkov_report.json"
    trivy_file = "artifacts/trivy_report.json"

    # Explain Checkov findings
    if os.path.exists(checkov_file):
        checkov_data = load_findings(checkov_file)
        failed_checks = checkov_data.get("results", {}).get("failed_checks", [])
        explain_and_log(failed_checks, "Checkov")
    else:
        print(f"[Warning] {checkov_file} not found.")

    # Explain Trivy findings
    if os.path.exists(trivy_file):
        trivy_data = load_findings(trivy_file)
        trivy_results = trivy_data.get("Results", [])
        explain_and_log(trivy_results, "Trivy")
    else:
        print(f"[Warning] {trivy_file} not found.")
