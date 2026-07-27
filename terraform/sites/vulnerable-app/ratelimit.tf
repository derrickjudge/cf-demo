resource "cloudflare_ruleset" "rate_limit" {
  zone_id = cloudflare_zone.this.id
  name    = "Rate limiting for cf-demo-vulnerable-app"
  kind    = "zone"
  phase   = "http_ratelimit"

  rules = [{
    ref         = "rate_limit_login"
    description = "Rate limit POST /api/login by IP"
    expression  = "(http.request.uri.path eq \"/api/login\" and http.request.method eq \"POST\")"
    action      = "block"
    ratelimit = {
      characteristics     = ["cf.colo.id", "ip.src"]
      period              = 60
      requests_per_period = 10
      mitigation_timeout  = 600
    }
  }]
}
