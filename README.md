# Cloudflare Application Security Demo

Runbook in progress — this file will capture every command needed to rebuild
this demo from scratch, in order, with `[Dashboard]` marking the handful of
steps Cloudflare requires through the console and `[CLI]` marking everything
else. Filled in phase by phase as the corresponding piece is built:

- [ ] Prerequisites (tools, accounts)
- [ ] Terraform state backend (R2) setup
- [ ] Terraform foundation (provider, variables)
- [ ] Vulnerable Worker: local dev and first deploy
- [ ] WAF + rate-limit rules for the vulnerable-app zone
- [ ] mtpcollective.com onboarding (including the manual nameserver cutover)
- [ ] CI/CD: GitHub Actions secrets and workflows
- [ ] Demo script: exact commands for the live before/after
