import json
from typing import List

from .config import SEVERITY_ORDER
from .scanner import Finding


def render_text(findings: List[Finding], target: str) -> str:
    lines = []
    lines.append("SecretScanner")
    lines.append("")
    lines.append(f"Scanning: {target}")
    lines.append("")

    if not findings:
        lines.append("No secrets found.")
        return "\n".join(lines)

    ordered = sorted(
        findings,
        key=lambda f: (SEVERITY_ORDER.get(f.severity, 99), f.file, f.line),
    )

    for finding in ordered:
        lines.append(f"[{finding.severity}] {finding.detector}")
        lines.append(f"  File: {finding.file}")
        lines.append(f"  Line: {finding.line}")
        lines.append(f"  Value: {finding.masked_value}")
        lines.append("")

    lines.append("-" * 28)
    lines.append(f"{len(findings)} possible secret(s) found.")
    return "\n".join(lines)


def render_json(findings: List[Finding], target: str) -> str:
    payload = {
        "target": target,
        "total_findings": len(findings),
        "findings": [
            {
                "file": f.file,
                "line": f.line,
                "detector": f.detector,
                "severity": f.severity,
                "masked_value": f.masked_value,
            }
            for f in findings
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)
