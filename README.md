# Cloudflare Application Security Demo

Two live stories, both driven entirely by GitHub -> Terraform -> Cloudflare:

1. **IaC-driven security, real CI/CD**: a small intentionally-vulnerable
   Python Worker (`letmeshowthevalue.com`), protected by WAF custom rules
   and rate limiting -- every change to those rules is a Terraform edit,
   a push, and a pipeline run, not a dashboard click.
2. **Painless onboarding of an existing site**: a real, live personal site
   (`mtpcollective.com`, hosted on Vercel) pulled under Cloudflare's control
   with zero downtime and zero loss of email.

`[CLI]` = run this yourself. `[Dashboard]` = the handful of steps Cloudflare
genuinely requires through the console. Everything else is Terraform/GitHub
Actions.

## Prerequisites

- `[CLI]` Node.js (repo tested with the system default, currently v26) and
  npm.
- `[CLI]` A second, older Node.js for the Python Worker toolchain specifically
  -- see the "Python Workers gotcha" note below. Install via Homebrew as a
  **keg-only** formula so it never becomes your system default:
  ```bash
  brew install node@24
  ```
- `[CLI]` [`uv`](https://docs.astral.sh/uv/) for the Python Worker's package
  management (`pywrangler`).
- `[CLI]` Terraform, via HashiCorp's own tap (Homebrew core dropped the
  official formula after HashiCorp's license change):
  ```bash
  brew tap hashicorp/tap
  brew install hashicorp/tap/terraform
  ```
- `[CLI]` `gh` (GitHub CLI), authenticated (`gh auth login`).
- A Cloudflare account. **If you have access to more than one account under
  the same login**, confirm the correct account ID before doing anything --
  `wrangler` will error non-interactively if it can't disambiguate:
  ```bash
  wrangler whoami        # lists every account this login can access
  export CLOUDFLARE_ACCOUNT_ID=<the correct one>
  ```

## Repo-local tooling (no global installs)

`wrangler` is a repo-local dependency, not a global install, so versions
stay pinned and reproducible:

```bash
npm install                       # installs wrangler per package.json
npx wrangler --version            # confirm it works
```

The first `npm install` will likely warn about blocked postinstall scripts
for `esbuild` and `workerd` (npm's supply-chain protection). Both are
legitimate and required -- `workerd` is the actual Workers runtime used for
local dev, `esbuild` bundles the Worker for deploy:

```bash
npm approve-scripts esbuild workerd
```

## 1. `[Dashboard]` Cloudflare API tokens

Two **separate** credentials, least-privilege, never reused for each other:

**Main token** (`CLOUDFLARE_API_TOKEN`) -- used by both the Terraform
`cloudflare` provider and `wrangler`/`pywrangler` Worker deploys. Create via
**My Profile -> API Tokens -> Create Custom Token** with:

| Scope | Permission |
|---|---|
| Account | Workers Scripts: Edit |
| Account | D1: Edit |
| Account | Account Settings: Read |
| Zone | Zone: Edit |
| Zone | DNS: Edit |
| Zone | Zone Settings: Edit |
| Zone | Zone WAF: Edit |

(Workers Scripts:Edit is easy to miss and causes a confusing
`Authentication error [code: 10000]` on deploy if left out.)

**R2 token** (`R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY`) -- used *only* by
Terraform's `s3` backend to reach R2's S3-compatible API for state storage.
Create as an **Account API Token** (not User -- account tokens survive
independent of any one person's account membership) via **R2 -> Manage R2
API Tokens**, scoped to **Object Read & Write** on just the state bucket.

Store both locally in a gitignored `.env` (never commit, never paste into
chat with an AI assistant -- edit the file directly yourself):

```bash
CLOUDFLARE_ACCOUNT_ID=<account id>
CLOUDFLARE_API_TOKEN=<main token>
R2_ACCESS_KEY_ID=<r2 access key>
R2_SECRET_ACCESS_KEY=<r2 secret key>
```

## 2. `[CLI]` Terraform state backend (R2)

The bucket that stores Terraform's own state can't be created by Terraform
itself (same chicken-and-egg problem as an S3 backend on AWS) -- bootstrap
it once, manually:

```bash
npx wrangler r2 bucket create cf-demo-tfstate
```

R2 must be enabled on the account first (`[Dashboard]`: R2 Object Storage ->
enable, one-time, per account).

`terraform/versions.tf` points the `s3` backend at R2's endpoint
(`https://<ACCOUNT_ID>.r2.cloudflarestorage.com`) with the usual
`skip_credentials_validation`-style flags (R2 isn't real AWS STS). The
access key/secret are deliberately **not** in that file -- Terraform
backend blocks can't reference variables, so they're supplied at init time:

```bash
cd terraform
set -a; source ../.env; set +a
terraform init \
  -backend-config="access_key=$R2_ACCESS_KEY_ID" \
  -backend-config="secret_key=$R2_SECRET_ACCESS_KEY"
```

State locking (`use_lockfile`) is deliberately left off -- it depends on S3
conditional writes that R2 doesn't confirm supporting for plain `PutObject`.
Fine for a solo-operator setup; revisit if this ever needs concurrent
applies.

## 3. `[CLI]` GitHub Actions secrets

```bash
gh secret set CLOUDFLARE_API_TOKEN --repo <owner>/cf-demo    # reads from stdin
gh secret set CLOUDFLARE_ACCOUNT_ID --repo <owner>/cf-demo
gh secret set R2_ACCESS_KEY_ID --repo <owner>/cf-demo
gh secret set R2_SECRET_ACCESS_KEY --repo <owner>/cf-demo
```

(Pipe each value in via `echo -n "$VALUE" | gh secret set NAME`, sourced
from `.env` -- never typed or echoed directly.)

## 4. CI/CD-first, not "build everything then wire CI/CD on at the end"

Industry-standard order, and what this repo actually follows: the *only*
manual step is the R2 bootstrap above (a pipeline can't create the thing it
depends on). Everything else -- every zone, every DNS record, every WAF
rule -- gets applied via GitHub Actions (`.github/workflows/terraform.yml`,
`.github/workflows/deploy-worker.yml`), proven against the disposable
`letmeshowthevalue.com` zone first, before ever touching the real
`mtpcollective.com` site. Local `terraform plan`/`validate` while iterating
is normal; `apply` happens in CI.

Both workflows include `workflow_dispatch:` so they can be run on demand:

```bash
gh workflow run terraform.yml --repo <owner>/cf-demo
gh workflow run deploy-worker.yml --repo <owner>/cf-demo
```

(Needed once, for the very first push to a brand-new empty repo: GitHub
can't diff against a nonexistent parent commit, so path-filtered `push`
triggers silently don't fire on that first push. Every push after that
works normally.)

## 5. Python Workers gotcha: `pywrangler`, not bare `wrangler`

Plain `wrangler dev`/`deploy` does **not** vendor the `workers` Python SDK
module on its own -- you need `pywrangler` (from the `workers-py` PyPI
package, via `uv`):

```bash
cd vulnerable-app
# pyproject.toml already declares workers-py + workers-runtime-sdk as dev deps
uv run pywrangler dev      # local dev, seeds against --local D1 emulation
uv run pywrangler deploy   # real deploy
```

**Node version matters here.** A very new Node (this machine's system
default, v26) fails with `node: bad option: --experimental-wasm-stack-
switching` -- that V8 flag graduated out of experimental and newer Node
dropped it, but the Pyodide toolchain `workers-py` downloads still passes
it. Fix: prepend the keg-only Node 24 to `PATH` just for this command:

```bash
export PATH="/opt/homebrew/opt/node@24/bin:$PATH"
uv run pywrangler dev
```

GitHub Actions' `deploy-worker.yml` pins `actions/setup-node@v4` to
`node-version: "24"` for the same reason.

## 6. Vulnerable-app zone (`letmeshowthevalue.com`)

If you're repeating this against a *new* throwaway domain, register it
through Cloudflare directly (this one auto-onboarded as an active zone with
zero manual nameserver work) or through any registrar and follow the same
nameserver flow as mtpcollective.com below.

Terraform (`terraform/sites/vulnerable-app/`) creates, in order:
- `cloudflare_zone`
- `cloudflare_d1_database` -- **not** `wrangler d1 create`; keeps the
  database itself in the IaC story. Declare `read_replication = { mode =
  "disabled" }` explicitly -- leaving it unset makes Terraform try to PUT
  it back to `null` on every apply, which the API rejects.
- `cloudflare_workers_custom_domain` -- binds the zone to the deployed
  Worker. Requires the Worker to already exist (deploy it first).
- `cloudflare_ruleset` (phase `http_request_firewall_custom`) -- the actual
  WAF block rule.
- `cloudflare_ruleset` (phase `http_ratelimit`) -- rate limiting.

Seed the **real remote** D1 database once (local `--local` dev has its own
separate SQLite emulation and needs its own seed):

```bash
npx wrangler d1 execute cf-demo-vulnerable-app-db --remote --file=schema.sql
```

**WAF rule gotcha**: `http.request.uri.query` (and the `args`/`args.names`/
`args.values` fields) are raw/undecoded in Cloudflare's rules language.
A rule written as `http.request.uri.query contains "<script"` will **not**
match a URL-encoded payload (`%3Cscript`) -- wrap the field in
`url_decode()` first, or percent-encoded attacks silently sail through a
rule that looks correct and tests fine against an unencoded payload.

**Rate-limit gotcha**: the Free plan restricts rate limiting rules to a
**10-second period and a matching 10-second mitigation timeout** --
anything else (e.g. 60s/600s) is rejected by the API with `not entitled to
use the period 60, can only use a period among [10]`. Also: Cloudflare's
rate-limit counter is distributed/eventually-consistent across the edge, so
enforcement isn't deterministic to an exact request number -- send a burst
(10+ requests) rather than expecting it to trip on request N precisely.

**Real demo login**: `POST /api/login` succeeds only for username `djudge`,
checked against a `DEMO_LOGIN_PASSWORD` Worker secret -- never committed,
set once per environment:

```bash
cd vulnerable-app
npx wrangler secret put DEMO_LOGIN_PASSWORD   # prompts, doesn't echo
```

For local `wrangler dev`, set the same variable in a git-ignored
`vulnerable-app/.dev.vars` (`DEMO_LOGIN_PASSWORD="..."`) instead. Every other
credential -- including the seed users below, whose password_hash values are
fabricated -- still 401s, which is what drives the rate-limit demo.

## 7. mtpcollective.com onboarding (the real, live site)

**Before touching anything**: inventory every existing record so nothing
(especially mail) gets dropped, and confirm DNSSEC is off (a common cause
of post-cutover breakage):

```bash
for type in A AAAA CNAME MX TXT NS CAA; do
  echo "=== $type ==="; dig +short mtpcollective.com $type
done
dig +short mtpcollective.com DS    # empty = DNSSEC not enabled, good
```

Terraform (`terraform/sites/mtpcollective/`) replicates every record found
this way -- **using the actual current IPs from `dig`, not a generic value
from a tutorial** (Vercel's own docs explicitly warn: "verify against your
domain card rather than reusing an IP from another guide" -- their anycast
IPs are assigned per-project and do differ). `www` uses a `CNAME` to
`cname.vercel-dns.com` rather than replicating Vercel's own hardcoded A
records for that subdomain, since a CNAME is Vercel's recommended,
more-resilient pattern for subdomains (the apex can't be a CNAME at all --
that's a DNS protocol rule, which is why Vercel's apex guidance is a static
anycast A record instead).

**SSL/TLS mode gotcha**: set to `"full"`, **not** `"strict"`
(`cloudflare_zone_setting`, `setting_id = "ssl"`). "Full (strict)" requires
the origin to already present a certificate Cloudflare's edge trusts --
but Vercel can't *issue* that certificate until domain verification
completes, which requires traffic to reach it first through the proxy.
Starting with `"strict"` walks straight into that chicken-and-egg failure
(a real, documented Vercel Community issue). Upgrading to `"strict"` is
safe *after* Vercel has successfully issued its own certificate post-
cutover.

**CAA check**: if the domain has existing CAA records, confirm they permit
at least one of Cloudflare's partner CAs (`letsencrypt.org`, `pki.goog`,
`ssl.com`, `sectigo.com`) or cert issuance will be blocked outright.

Terraform creates the zone and outputs the assigned nameservers:

```bash
terraform output mtpcollective_name_servers
```

**`[Dashboard/registrar]` The one genuinely manual, hard-to-reverse step**:
take those nameserver values to wherever the domain is actually
*registered* (not necessarily the same as its current DNS host -- confirm
which before assuming the Vercel dashboard is the right place). For a
domain both registered and DNS-hosted at Vercel: **Vercel Dashboard ->
Domains -> your domain -> Nameservers -> Use Custom Nameservers**.

After the cutover, verify:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://mtpcollective.com
curl -s -o /dev/null -w "%{http_code}\n" https://www.mtpcollective.com
dig +short mtpcollective.com MX      # mail still intact
dig +short mtpcollective.com TXT     # SPF / verification still intact
```

## 8. Demo scripts

```bash
demo/trigger-sqli.sh [host]         # default host: https://letmeshowthevalue.com
demo/trigger-xss.sh [host]
demo/trigger-ratelimit.sh [host] [count]   # default count: 10
```

Each shows the normal-use response in full (the "proof of exploit" moment
when unprotected), and just the status code once the WAF/rate-limit rules
are blocking it (Cloudflare's block page HTML is long and not worth
reading aloud live).

**The live CI/CD moment**: run a trigger script (200/data leaks), comment
out or loosen the block rule in `terraform/sites/vulnerable-app/waf.tf`,
push, watch `terraform.yml` run in Actions, run the same script again
(403). Same command, different result -- that's the whole pitch.
