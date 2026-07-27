#!/usr/bin/env bash
# Fires a normal /search request, then a SQL injection payload, against the
# vulnerable-app Worker. Before the WAF custom rule is deployed, the
# injection dumps every row in `users` (including admin's password hash).
# After, it should return 403 (Cloudflare's own block page, not shown in
# full here -- just confirmed by status code).
set -euo pipefail

HOST="${1:-https://letmeshowthevalue.com}"

echo "=== Normal use: ${HOST}/search?q=alice ==="
curl -s -w "\nHTTP %{http_code}\n" "${HOST}/search?q=alice"

echo ""
echo "=== SQL injection payload: q=' OR '1'='1 ==="
code=$(curl -s -o /tmp/cf-demo-sqli-response.html -w "%{http_code}" "${HOST}/search?q=%27%20OR%20%271%27%3D%271")
if [ "${code}" = "403" ]; then
  echo "HTTP 403 -- blocked by WAF custom rule"
else
  echo "HTTP ${code} -- NOT blocked, response body:"
  cat /tmp/cf-demo-sqli-response.html
fi
rm -f /tmp/cf-demo-sqli-response.html
