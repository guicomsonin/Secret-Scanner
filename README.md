# SecretScanner

Fast, lightweight secret scanner for developers.

SecretScanner walks through your project files looking for exposed secrets
such as API keys, tokens and private keys, and reports where they were
found without ever printing the full secret value.

## Install

```bash
pip install secretscanner
```

Or, from source:

```bash
git clone https://github.com/your-user/secretscanner.git
cd secretscanner
pip install -e .
```

## Usage

Scan the current directory:

```bash
secretscanner .
```

Scan a single file:

```bash
secretscanner .env
```

Exclude a directory:

```bash
secretscanner . --exclude node_modules
```

Exclude a file extension:

```bash
secretscanner . --exclude-ext .log
```

Output as JSON:

```bash
secretscanner . --format json
```

CI mode (exits with code 1 if any secret is found):

```bash
secretscanner . --ci
```

## GitHub Actions example

```yaml
- name: Scan secrets
  run: |
    pip install secretscanner
    secretscanner . --ci
```

## What it detects (v0.1)

- AWS Access Key and Secret Key
- GitHub Token (classic and fine-grained)
- OpenAI API Key
- Slack Token
- JWT
- Private key blocks (`-----BEGIN ... PRIVATE KEY-----`)
- Generic assignments to `API_KEY`, `SECRET`, `TOKEN`, `PASSWORD`, `PRIVATE_KEY`

By default, `.git`, `node_modules`, `venv`, `.venv`, `env`, `__pycache__`,
`dist`, `build`, `.idea`, `.vscode` and `target` are excluded from scans.

## Roadmap

- v0.2: entropy detection, `.gitignore` support, SARIF output
- v0.3: scan Git history
- v0.4: dedicated GitHub Action
- v0.5: pre-commit hook
- v1.0: custom rules and plugins

## Contributing

Issues and pull requests are welcome.

## License

This project is licensed under the GNU General Public License v3.0 or later.
See the [LICENSE](LICENSE) file for details.
