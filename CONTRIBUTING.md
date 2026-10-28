# Contributing to Falvorn AI

Falvorn AI is at the **private alpha / independent MVP** stage. Contributions should begin with a GitHub issue and a small, reviewable pull request. The repository has no open-source license at this stage; do not infer a right to redistribute it. Maintainers can choose licensing separately.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Use `python -m falvorn` after configuring `.env` for local running. Preserve the existing SSRF and browser-action safety checks; avoid adding CAPTCHA bypass, stealth evasion, credential scraping, or automatic consequential transactions. Never commit `.env`, tokens, cookies, real customer data, session recordings, or private-site dumps.

Report vulnerabilities privately according to [SECURITY.md](SECURITY.md).
