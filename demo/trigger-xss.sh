#!/usr/bin/env bash
# Fires a normal /greet request, then an XSS payload, against the
# vulnerable-app Worker. Before the WAF custom rule is deployed, the
# payload is reflected unescaped in the HTML response. After, it should
# return 403 (Cloudflare's own block page, not shown in full here -- just
# confirmed by status code).
set -euo pipefail

HOST="${1:-https://letmeshowthevalue.com}"

echo "=== Normal use: ${HOST}/greet?name=world ==="
curl -s -w "\nHTTP %{http_code}\n" "${HOST}/greet?name=world"

echo ""
echo "=== XSS payload: name=<script>alert(1)</script> ==="
code=$(curl -s -o /tmp/cf-demo-xss-response.html -w "%{http_code}" "${HOST}/greet?name=%3Cscript%3Ealert(1)%3C%2Fscript%3E")
if [ "${code}" = "403" ]; then
  echo "HTTP 403 -- blocked by WAF custom rule"
else
  echo "HTTP ${code} -- NOT blocked, response body:"
  cat /tmp/cf-demo-xss-response.html
fi
rm -f /tmp/cf-demo-xss-response.html
