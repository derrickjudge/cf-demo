#!/usr/bin/env bash
# Generates a realistic mix of traffic against the vulnerable-app demo site
# so Cloudflare Analytics / Security Events have real data to show during
# the presentation, rather than an empty dashboard: legitimate page views,
# scanner-style probes against nonexistent paths (the kind of background
# internet noise every public site gets), and login attempts.
#
# Usage: demo/generate-load.sh [host] [duration_seconds] [requests_per_second]
set -euo pipefail

HOST="${1:-https://letmeshowthevalue.com}"
DURATION="${2:-120}"
RPS="${3:-2}"

VALID_PAGES=(
  "/login"
  "/dashboard"
  "/customers"
  "/product"
  "/solutions"
  "/pricing"
  "/contact"
  "/greet?name=Alice"
  "/search?q=bob"
)

# Classic scanner/bot probe paths -- none of these exist on this Worker, so
# they all 404, but they're exactly what real internet background-noise
# scanning looks like in server logs.
SCAN_PATHS=(
  "/wp-admin/"
  "/wp-login.php"
  "/.env"
  "/.git/config"
  "/admin"
  "/administrator"
  "/phpmyadmin"
  "/xmlrpc.php"
  "/.aws/credentials"
  "/config.php"
  "/_profiler"
  "/server-status"
  "/vendor/.env"
  "/wp-content/debug.log"
  "/.ssh/id_rsa"
  "/actuator/health"
  "/telescope/requests"
  "/.well-known/traversal/../../etc/passwd"
)

LOGIN_USERNAMES=("djudge" "admin" "root" "test" "administrator")
LOGIN_PASSWORDS=("password123" "letmein" "admin123" "changeme" "qwerty")

count=0
trap 'echo ""; echo "Stopped -- sent ${count} requests."; exit 0' INT

end_time=$(( $(date +%s) + DURATION ))
echo "Generating mixed load against ${HOST} for ${DURATION}s (~${RPS} req/s, Ctrl+C to stop early)..."
echo ""

while [ "$(date +%s)" -lt "${end_time}" ]; do
  category=$(( RANDOM % 10 ))

  if [ "${category}" -lt 6 ]; then
    # 60% legitimate traffic
    path="${VALID_PAGES[$((RANDOM % ${#VALID_PAGES[@]}))]}"
    code=$(curl -s -o /dev/null -w "%{http_code}" "${HOST}${path}")
    printf "[valid]  GET  %-30s -> %s\n" "${path}" "${code}"
  elif [ "${category}" -lt 9 ]; then
    # 30% scanner-style probes against nonexistent paths
    path="${SCAN_PATHS[$((RANDOM % ${#SCAN_PATHS[@]}))]}"
    code=$(curl -s -o /dev/null -w "%{http_code}" "${HOST}${path}")
    printf "[scan]   GET  %-30s -> %s\n" "${path}" "${code}"
  else
    # 10% login attempts, effectively all wrong credentials
    user="${LOGIN_USERNAMES[$((RANDOM % ${#LOGIN_USERNAMES[@]}))]}"
    pass="${LOGIN_PASSWORDS[$((RANDOM % ${#LOGIN_PASSWORDS[@]}))]}"
    code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${HOST}/api/login" \
      -H "content-type: application/json" \
      -d "{\"username\":\"${user}\",\"password\":\"${pass}\"}")
    printf "[login]  POST /api/login (%-12s) -> %s\n" "${user}" "${code}"
  fi

  count=$((count + 1))
  delay=$(echo "scale=2; (1/${RPS}) * (0.5 + ${RANDOM}/32767)" | bc)
  sleep "${delay}"
done

echo ""
echo "Done -- sent ${count} requests over ${DURATION}s."
