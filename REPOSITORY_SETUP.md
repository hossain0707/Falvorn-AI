# Publish Falvorn AI to GitHub

**Owner:** `hossain0707`  
**Repository:** `Falvorn-AI`  
**Suggested visibility:** Private until licensing and security review are complete  
**Description:** `Falvorn AI — autonomous browser agents, secure web automation, search and developer APIs.`  
**Default branch:** `main`

## GitHub web creation

1. Open https://github.com/new and select your personal account `hossain0707` as owner.
2. Enter `Falvorn-AI` and the description above. Choose **Private** initially.
3. Leave **Initialize repository with README**, **.gitignore** and **license** unchecked (this package already includes the first two; licensing is undecided).
4. Create the empty repository.
5. In the unpacked source folder execute:

```bash
git init -b main
git add .
git commit -m "feat: initialize Falvorn AI v0.1"
git remote add origin https://github.com/hossain0707/Falvorn-AI.git
git push -u origin main
```

Authenticate using your credential manager or GitHub CLI/browser auth. Never paste a personal access token in chat or commit it to files. The connected GitHub connector can manage files and PRs once the repository exists.

## Recommended GitHub settings after creation

- Require pull requests and CI checks before merging to `main` once collaborators join.
- Enable dependency alerts and secret scanning if available for your plan.
- Add `good first issue`, `enhancement`, `bug`, `security` labels and a milestone for v0.2.
- Configure repository Discussions only if you want a public developer community.
- Do not publish production credentials, active cookies or private customer browsing logs.
