from pathlib import Path

from secretscanner.scanner import Scanner


def test_scan_directory_finds_secrets(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "config.js").write_text(
        'const key = "AKIAABCDEFGHIJKLMNOP";\n'
    )
    (project / "clean.py").write_text("print('hello world')\n")

    excluded = project / "node_modules"
    excluded.mkdir()
    (excluded / "leaked.js").write_text('const t = "AKIAABCDEFGHIJKLMNOP";\n')

    scanner = Scanner(target=str(project))
    findings = scanner.scan()

    files_with_findings = {f.file for f in findings}
    assert any("config.js" in f for f in files_with_findings)
    assert not any("node_modules" in f for f in files_with_findings)


def test_scan_single_file(tmp_path: Path):
    file_path = tmp_path / ".env"
    file_path.write_text("SECRET=my-super-secret-value-123456\n")

    scanner = Scanner(target=str(file_path))
    findings = scanner.scan()

    assert len(findings) >= 1
    assert findings[0].file == str(file_path)


def test_custom_exclude_dir(tmp_path: Path):
    project = tmp_path / "project"
    (project / "skip_me").mkdir(parents=True)
    (project / "skip_me" / "secret.txt").write_text(
        "TOKEN=abcdefghijklmnop123456\n"
    )

    scanner = Scanner(target=str(project), exclude_dirs={"skip_me"})
    findings = scanner.scan()

    assert findings == []
