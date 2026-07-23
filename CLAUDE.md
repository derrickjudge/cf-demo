Rigor: poc
Hosting: managed-cloud

# Cloudflare Application Security Demo

A customer-facing demo of Cloudflare's application-security platform: an
IaC-driven CI/CD pipeline (GitHub -> Terraform -> Cloudflare) for managing WAF
and rate-limiting config, plus onboarding a real existing site
(mtpcollective.com, currently on Vercel) under Cloudflare's control. See
`README.md` for the full command-by-command runbook.

Per the `poc` rigor level declared above, tests are deferred — the
functional verification for this project is the live `curl` before/after
demo in `demo/`, not a unit test suite. State explicitly (as here) whenever
that's the case, per the global CLAUDE.md.

## Layout

- `terraform/` — IaC for both Cloudflare zones (the real site, and the
  throwaway domain fronting the vulnerable app). Remote state lives in an R2
  bucket (see `terraform/versions.tf`).
- `vulnerable-app/` — a small, intentionally-vulnerable Python (Pyodide)
  Worker, D1-backed. Bait for the WAF/rate-limit demo — not a real app.
- `demo/` — `curl` scripts that trigger each vulnerability on demand.
- `.github/workflows/` — CI: `terraform plan`/`apply`, and Worker deploy via
  `wrangler-action`.

## Secrets

Never commit `.env`, `*.tfvars`, or any Cloudflare/R2 credentials. GitHub
Actions secrets: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`,
`R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`. See `README.md` for scopes and
how each is created.
