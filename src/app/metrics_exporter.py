from fastapi import FastAPI, Response
import os
import re

app = FastAPI()

LOG_FILE = "logs/ai_explanation.log"


def parse_ai_log():
    if not os.path.exists(LOG_FILE):
        return {
            "checkov_summary_exists": 0,
            "trivy_summary_exists": 0,
            "summary_line_count": 0,
            "checkov_issue_count": 0,
            "trivy_issue_count": 0
        }

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.strip().splitlines()
    checkov_summary_exists = "=== Checkov Findings ===" in content
    trivy_summary_exists = "=== Trivy Findings ===" in content

    # Naive issue count estimation
    checkov_issues = len(re.findall(r"Checkov Finding \d+:", content, re.IGNORECASE))
    trivy_issues = len(re.findall(r"Trivy Finding \d+:", content, re.IGNORECASE))

    return {
        "checkov_summary_exists": int(checkov_summary_exists),
        "trivy_summary_exists": int(trivy_summary_exists),
        "summary_line_count": len(lines),
        "checkov_issue_count": checkov_issues,
        "trivy_issue_count": trivy_issues
    }


@app.get("/metrics")
def metrics():
    data = parse_ai_log()
    prometheus_format = f"""
# HELP auditai_checkov_summary_success Whether Checkov summary was generated
# TYPE auditai_checkov_summary_success gauge
auditai_checkov_summary_success {data["checkov_summary_exists"]}

# HELP auditai_trivy_summary_success Whether Trivy summary was generated
# TYPE auditai_trivy_summary_success gauge
auditai_trivy_summary_success {data["trivy_summary_exists"]}

# HELP auditai_summary_lines_total Number of lines in AI summary log
# TYPE auditai_summary_lines_total gauge
auditai_summary_lines_total {data["summary_line_count"]}

# HELP auditai_checkov_issue_count Number of Checkov issues summarized
# TYPE auditai_checkov_issue_count gauge
auditai_checkov_issue_count {data["checkov_issue_count"]}

# HELP auditai_trivy_issue_count Number of Trivy issues summarized
# TYPE auditai_trivy_issue_count gauge
auditai_trivy_issue_count {data["trivy_issue_count"]}
""".strip()

    return Response(content=prometheus_format, media_type="text/plain")
