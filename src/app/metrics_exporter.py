from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import os

app = FastAPI()

# Prometheus metrics
checkov_findings = Gauge("checkov_findings_total", "Total Checkov AI-explained security findings")
trivy_critical = Gauge("trivy_vulnerabilities_critical", "Critical vulnerabilities found by Trivy")
trivy_high = Gauge("trivy_vulnerabilities_high", "High vulnerabilities found by Trivy")

def parse_checkov_log(file_path):
    """
    Count 'FAILED' findings in Checkov analysis log.
    """
    if not os.path.exists(file_path):
        return 0

    with open(file_path, 'r') as f:
        content = f.read()
        return content.count("**Result:** FAILED")

def parse_trivy_log(file_path):
    """
    Count 'CRITICAL' and 'HIGH' findings in Trivy analysis log.
    """
    if not os.path.exists(file_path):
        return (0, 0)

    critical_count = 0
    high_count = 0
    with open(file_path, 'r') as f:
        for line in f:
            if "Severity: CRITICAL" in line:
                critical_count += 1
            elif "Severity: HIGH" in line:
                high_count += 1
    return critical_count, high_count

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    # Parse logs and update metrics
    checkov_total = parse_checkov_log("/app/logs/checkov_analysis.log")
    crit, high = parse_trivy_log("/app/logs/trivy_analysis.log")

    checkov_findings.set(checkov_total)
    trivy_critical.set(crit)
    trivy_high.set(high)

    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
