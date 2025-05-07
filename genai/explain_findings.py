import json
import os
from subprocess import run

# Function to call a local AI model (like llama3 or mistral) using the `ollama` CLI tool.
# The function sends a prompt to the model and retrieves the response.
def call_ollama(prompt):
    """Call local ollama model like llama3 or mistral."""
    # Run the `ollama` command with the specified model and prompt.
    # `capture_output=True` captures the output, and `text=True` ensures the output is in text format.
    result = run(["ollama", "run", "llama3", prompt], capture_output=True, text=True)
    # Return the model's response after stripping any extra whitespace.
    return result.stdout.strip()

# Function to load security findings from a JSON file.
# This function reads the file and parses its content into a Python dictionary.
def load_findings(file_path):
    # Open the specified file in read mode.
    with open(file_path, "r") as f:
        # Parse the JSON content of the file and return it as a Python dictionary.
        return json.load(f)

# Function to summarize and explain security findings using the AI model.
# It prepares a prompt with the findings and sends it to the AI model for explanation.
def summarize_findings(findings):
    # Create a prompt to explain the findings in plain English.
    explanation_prompt = "Summarize and explain these security findings in plain English:\n"
    # Add the first three findings (for brevity) to the prompt in a readable JSON format.
    explanation_prompt += json.dumps(findings[:3], indent=2)  # limit for brevity
    # Call the AI model with the prepared prompt and return the explanation.
    return call_ollama(explanation_prompt)

# Main block of the script. This is executed when the script is run directly.
if __name__ == "__main__":
    # Define the path to the Checkov scan report file.
    file = 'artifacts\\checkov_report.json'
    
    # Check if the scan report file exists.
    if os.path.exists(file):
        # Load the findings from the report file.
        findings = load_findings(file)
        # Extract the failed checks from the findings and summarize them using the AI model.
        summary = summarize_findings(findings.get("results", {}).get("failed_checks", []))
        # Print the AI-generated explanation of the findings.
        print("\nAI Explanation of Findings:\n", summary)
    else:
        # Print a warning message if the scan report file is not found.
        print("Scan report not found.")