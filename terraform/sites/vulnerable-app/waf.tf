resource "cloudflare_ruleset" "custom_rules" {
  zone_id = cloudflare_zone.this.id
  name    = "Custom rules for cf-demo-vulnerable-app"
  kind    = "zone"
  phase   = "http_request_firewall_custom"

  rules = [{
    ref         = "block_sqli_xss_demo_payloads"
    description = "Block the specific SQLi/XSS payloads this demo sends"
    expression  = "(http.request.uri.path eq \"/search\" and url_decode(http.request.uri.query) contains \"'\") or (http.request.uri.path eq \"/greet\" and url_decode(http.request.uri.query) contains \"<script\")"
    action      = "block"
  }]
}
