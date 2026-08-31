import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Detector:
    name: str
    severity: str
    pattern: re.Pattern


DETECTORS = [
    Detector(
        name="AWS Access Key",
        severity="CRITICAL",
        pattern=re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    ),
    Detector(
        name="AWS Secret Key",
        severity="CRITICAL",
        pattern=re.compile(
            r"(?i)aws_secret_access_key\s*[=:]\s*[\"']?[A-Za-z0-9/+=]{40}[\"']?"
        ),
    ),
    Detector(
        name="GitHub Token",
        severity="HIGH",
        pattern=re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b"),
    ),
    Detector(
        name="GitHub Fine-Grained Token",
        severity="HIGH",
        pattern=re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,255}\b"),
    ),
    Detector(
        name="OpenAI API Key",
        severity="HIGH",
        pattern=re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    ),
    Detector(
        name="Slack Token",
        severity="HIGH",
        pattern=re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    ),
    Detector(
        name="JWT",
        severity="MEDIUM",
        pattern=re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    ),
    Detector(
        name="Private Key Block",
        severity="CRITICAL",
        pattern=re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ),
    Detector(
        name="Generic Secret Assignment",
        severity="MEDIUM",
        pattern=re.compile(
            r"(?i)\b(api[_-]?key|secret|token|password|passwd|private[_-]?key)\b"
            r"\s*[=:]\s*[\"']?[A-Za-z0-9/+_\-=]{8,}[\"']?"
        ),
    ),
]


def mask_value(value: str, visible: int = 4) -> str:
    if len(value) <= visible:
        return "*" * len(value)
    return value[:visible] + "*" * max(len(value) - visible, 0)
