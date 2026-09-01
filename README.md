# SecretScanner

**Fast, lightweight secret scanner for developers.**

SecretScanner walks through your project files looking for exposed secrets such as API keys, tokens and private keys, and reports where they were found **without printing the full secret value**.

## 🔍 Demo

Run SecretScanner against a project:

```bash
secretscanner .
```

Example output:

```text
SecretScanner

Scanning: .

[CRITICAL] AWS Access Key
  File: tests/test_detectors.py
  Line: 9
  Value: AKIA****************

[CRITICAL] Private Key Block
  File: tests/test_detectors.py
  Line: 26
  Value: ----***************************

[HIGH] OpenAI API Key
  File: tests/test_detectors.py
  Line: 17
  Value: sk-a***********************************

[MEDIUM] JWT
  File: tests/test_detectors.py
  Line: 21
  Value: eyJh********************************************************

----------------------------
12 possible secret(s) found.
```

SecretScanner masks detected values to prevent the full secret from being exposed in terminal output.

## ✨ Features

* 🔎 Scan entire directories or individual files
* 🔐 Detect common API keys, tokens and private keys
* 🛡️ Mask detected secrets in output
* 📁 Exclude directories and file extensions
* 📄 JSON output support
* ⚙️ CI mode for automated security checks
* 🚀 Lightweight and fast
* 🐍 Python-based CLI

## 📦 Install

```bash
pip install secretscanner
```

Or install directly from source:

```bash
git clone https://github.com/guicomsonin/Secret-Scanner.git
cd Secret-Scanner
pip install -e .
```

## 🚀 Usage

### Scan the current directory

```bash
secretscanner .
```

### Scan a single file

```bash
secretscanner .env
```

### Exclude a directory

```bash
secretscanner . --exclude node_modules
```

### Exclude a file extension

```bash
secretscanner . --exclude-ext .log
```

### Output as JSON

```bash
secretscanner . --format json
```

### CI mode

CI mode exits with code `1` if any possible secret is detected:

```bash
secretscanner . --ci
```

This makes SecretScanner suitable for automated security checks and CI/CD pipelines.

## 🤖 GitHub Actions

Example workflow:

```yaml
- name: Scan secrets
  run: |
    pip install secretscanner
    secretscanner . --ci
```

## 🔐 What It Detects

### v0.1

* AWS Access Key and Secret Key
* GitHub Token (classic and fine-grained)
* OpenAI API Key
* Slack Token
* JWT
* Private key blocks (`-----BEGIN ... PRIVATE KEY-----`)
* Generic assignments to:

  * `API_KEY`
  * `SECRET`
  * `TOKEN`
  * `PASSWORD`
  * `PRIVATE_KEY`

By default, the following directories are excluded:

```text
.git
node_modules
venv
.venv
env
__pycache__
dist
build
.idea
.vscode
target
```

## 🗺️ Roadmap

* [x] Basic secret detection
* [x] CLI interface
* [x] JSON output
* [x] CI mode
* [ ] v0.2 — Entropy detection
* [ ] v0.2 — `.gitignore` support
* [ ] v0.2 — SARIF output
* [ ] v0.3 — Git history scanning
* [ ] v0.4 — Dedicated GitHub Action
* [ ] v0.5 — Pre-commit hook
* [ ] v1.0 — Custom rules and plugins

## 🤝 Contributing

Issues and pull requests are welcome.

If you find a bug, false positive, or have an idea for a new detector, feel free to open an issue or submit a pull request.

## 📄 License

Copyright © 2026 Guilherme

SecretScanner is free and open-source software licensed under the **GNU General Public License v3.0 or later**.

See the [LICENSE](LICENSE) file for the full license text.
