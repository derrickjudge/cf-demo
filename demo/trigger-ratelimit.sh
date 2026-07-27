#!/usr/bin/env bash
# Hammers POST /api/login to trigger the rate-limit rule (5 requests/10s on
# the Free plan -- see terraform/sites/vulnerable-app/ratelimit.tf). Every
# request returns 401 (no real auth logic); once the rate limit trips,
# responses flip to 429 until the 10s mitigation window expires.
#
# Note: Cloudflare's rate-limit counter is distributed/eventually-consistent
# across the edge, so the trip point isn't deterministic to an exact request
# number and enforcement can be intermittent rather than a hard block for the
# full window. Send enough requests (10+) to reliably see it trigger.
set -euo pipefail

HOST="${1:-https://letmeshowthevalue.com}"
COUNT="${2:-10}"

echo "Sending ${COUNT} POST requests to ${HOST}/api/login..."
for i in $(seq 1 "${COUNT}"); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${HOST}/api/login")
  echo "request ${i}: ${code}"
done
