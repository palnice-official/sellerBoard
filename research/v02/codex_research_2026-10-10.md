# ChatGPT Codex — facts used for the v0.3 build handoff (checked 2026-10-10)

Sources (official docs unless noted):
- C1 Cloud environments (current): https://learn.chatgpt.com/docs/environments/cloud-environments.md
- C2 Cloud environment (legacy): https://learn.chatgpt.com/docs/environments/cloud-environment
- C3 Internet access (legacy cloud): https://learn.chatgpt.com/docs/cloud/internet-access
- C4 Code review in GitHub: https://learn.chatgpt.com/docs/third-party/github
- C5 AGENTS.md guide: https://learn.chatgpt.com/docs/agent-configuration/agents-md.md
- C6 Using Codex cloud (Help Center): https://help.openai.com/en/articles/20001545-using-codex-cloud
- C7 TechCrunch 2026-09-29, reusable cloud environments (news): https://techcrunch.com/2026/09/29/openai-gives-codex-reusable-cloud-environments-that-work-across-devices/

## Environments (current experience, C1, C6)
- Create on web or desktop app (ChatGPT account): Work in → Cloud → Select environment → Create environment, or Settings → Codex Cloud → Environments. Select GitHub repositories (connect GitHub first). Codex inspects the repo, installs dependencies, tests the workflow, records an **Install script** and a **Start skill**; you review and **Publish**. Edits → Republish; only new tasks use the update.
- Each task runs in its own isolated VM; tasks continue while your computer sleeps; saved VM state recoverable up to 7 days after last turn — commit important work.
- VM defaults: Plus 2 vCPU/8 GiB/8 GiB disk; Pro/Business/Enterprise 4 vCPU/16 GiB/32 GiB.
- **Environment variables** are passed to programs. **Network secrets** are substituted by the proxy only for allowed HTTPS destinations (port 443) — programs see a placeholder. Personal values live in a Personal vault.
- Internet: toggle "Allow Codex to access internet"; allow-domain presets "Package managers", "Custom domains only", "All (unrestricted)" + additional allowed domains. Allowing a domain grants no credentials.
- Private networking: Tailscale only. OIDC short-lived cloud credentials: Enterprise by request. Agent egress IP feed published.
- Sharing: Privacy → Who can use (workspace or Only me). Admin permissions "Use Codex in the cloud", "Manage workspace environments".
- Not supported yet: computer/browser use, GitLab, GitHub Enterprise Server.
- Code Review, Security Review and GitHub/Linear integrations still run on Codex Cloud (Legacy) during the transition (C6).
- Not covered by the OpenAI BAA (no PHI) — irrelevant here, but do not put customer PII in tasks anyway.

## Legacy cloud facts still relevant for code review (C2, C3)
- Agent-phase internet off by default; setup scripts have internet. Allow-lists + only GET/HEAD/OPTIONS by default. Risks: prompt injection, exfiltration of code/secrets, malware, licence-restricted content.
- Legacy secrets available only to setup scripts, removed before the agent phase.

## Code review on GitHub (C4)
- Connect repo, turn on Automatic review, or comment `@codex review` on a PR. Codex flags only P0/P1 issues on GitHub.
- Review rules come from AGENTS.md section `## Code Review Rules` (root + nested files covering each changed file).
- `@codex fix the P1 issue` starts a task with the PR as context and can push a fix to the branch.

## AGENTS.md (C5)
- Discovery: global (~/.codex) then from repo root down to the working directory; per directory AGENTS.override.md > AGENTS.md > fallback names; concatenated root→leaf, later files override. Combined size cap `project_doc_max_bytes` = 32 KiB by default. Keep it concise; nest specialised guidance near the code.
