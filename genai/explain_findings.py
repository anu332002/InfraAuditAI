import json
import os
from subprocess import run

# File paths
TRIVY_REPORT = 'artifacts\\trivy_report.json'
CHECKOV_REPORT = 'artifacts\\checkov_report.json'
AI_LOG = 'logs\\ai_explanation.log'


def load_json_report(path):
    """Load JSON content from file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Report not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_ollama(prompt):
    """Run prompt through Ollama (Llama3)."""
    result = run(["ollama", "run", "llama3", prompt], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Ollama execution failed:\n{result.stderr}")
    return result.stdout.strip()


def summarize_trivy_findings(results):
    """Summarize vulnerabilities from Trivy JSON."""
    if not results:
        return "No Trivy findings to summarize."

    prompt_sections = []
    for result in results:
        target = result.get("Target", "Unknown Target")
        vulnerabilities = result.get("Vulnerabilities", [])
        if not vulnerabilities:
            continue

        prompt_sections.append(f"\nTarget: {target}")
        for vuln in vulnerabilities[:5]:  # limit to 5 per target
            prompt_sections.append(
                f"- {vuln.get('VulnerabilityID', 'N/A')} "
                f"({vuln.get('Severity', 'Unknown')}): "
                f"{vuln.get('Title', '')}"
            )

    if not prompt_sections:
        return "No vulnerabilities found in Trivy results."

    full_prompt = (
        "You are a DevSecOps expert. Review the following Docker image vulnerabilities "
        "found by Trivy. Explain each issue briefly and suggest mitigations:\n" +
        "\n".join(prompt_sections)
    )

    return run_ollama(full_prompt)


def summarize_checkov_findings(results):
    """Summarize failed checks from Checkov JSON."""
    failed = [r for r in results if r.get("check_result", {}).get("result") == "FAILED"]
    if not failed:
        return "No Checkov findings to summarize."

    prompt_sections = []
    for item in failed[:10]:  # limit to 10 failed checks
        resource = item.get("resource", "Unknown Resource")
        check_id = item.get("check_id", "N/A")
        check_name = item.get("check_name", "")
        file_path = item.get("file_path", "")
        prompt_sections.append(
            f"- {check_id} in {resource} ({file_path}): {check_name}"
        )

    full_prompt = (
        "You are a security analyst. Review the following infrastructure as code (IaC) "
        "misconfigurations found by Checkov. Explain the risks and provide remediations:\n" +
        "\n".join(prompt_sections)
    )

    return run_ollama(full_prompt)


def main():
    try:
        print("=== AI Explanation of Findings ===")

        # Trivy
        trivy_data = load_json_report(TRIVY_REPORT)
        trivy_summary = summarize_trivy_findings(trivy_data.get("Results", []))

        # Checkov
        checkov_data = load_json_report(CHECKOV_REPORT)
        checkov_summary = summarize_checkov_findings(checkov_data.get("results", {}).get("failed_checks", []))

        # Save results
        os.makedirs(os.path.dirname(AI_LOG), exist_ok=True)
        with open(AI_LOG, 'w', encoding='utf-8') as f:
            f.write("=== Trivy Scan Summary ===\n")
            f.write(trivy_summary + "\n\n")
            f.write("=== Checkov Scan Summary ===\n")
            f.write(checkov_summary + "\n")

        print(trivy_summary)
        print("\n" + checkov_summary)
        print(f"\n[✓] AI explanation saved to {AI_LOG}")

    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
