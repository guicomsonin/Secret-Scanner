import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Set

from .config import (
    DEFAULT_EXCLUDED_DIRS,
    DEFAULT_EXCLUDED_EXTENSIONS,
    MAX_FILE_SIZE_BYTES,
)
from .detectors import DETECTORS, mask_value


@dataclass
class Finding:
    file: str
    line: int
    detector: str
    severity: str
    masked_value: str


class Scanner:
    def __init__(
        self,
        target: str,
        exclude_dirs: Optional[Set[str]] = None,
        exclude_extensions: Optional[Set[str]] = None,
    ):
        self.target = Path(target)
        self.exclude_dirs = DEFAULT_EXCLUDED_DIRS | set(exclude_dirs or [])
        self.exclude_extensions = DEFAULT_EXCLUDED_EXTENSIONS | set(
            exclude_extensions or []
        )

    def scan(self) -> List[Finding]:
        findings: List[Finding] = []
        for file_path in self._iter_files():
            findings.extend(self._scan_file(file_path))
        findings.sort(key=lambda f: (f.file, f.line))
        return findings

    def _iter_files(self) -> Iterable[Path]:
        if self.target.is_file():
            yield self.target
            return

        for root, dirs, files in os.walk(self.target):
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            for filename in files:
                file_path = Path(root) / filename
                if file_path.suffix.lower() in self.exclude_extensions:
                    continue
                try:
                    if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
                        continue
                except OSError:
                    continue
                yield file_path

    def _scan_file(self, file_path: Path) -> List[Finding]:
        findings: List[Finding] = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except (OSError, UnicodeDecodeError):
            return findings

        for line_number, line in enumerate(lines, start=1):
            for detector in DETECTORS:
                match = detector.pattern.search(line)
                if not match:
                    continue
                findings.append(
                    Finding(
                        file=str(file_path),
                        line=line_number,
                        detector=detector.name,
                        severity=detector.severity,
                        masked_value=mask_value(match.group(0)),
                    )
                )
        return findings
