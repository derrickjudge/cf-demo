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
      # Free plan is restricted to a 10s period and a matching 10s
      # mitigation timeout (longer values are a paid plan feature) --
      # confirmed via API errors when 60s/600s were rejected.
      characteristics     = ["cf.colo.id", "ip.src"]
      period              = 10
      requests_per_period = 5
      mitigation_timeout  = 10
    }
    # Disabled for the live demo baseline -- flip back to true on stage to
    # show the protected state, pushed through the same CI/CD pipeline.
    enabled = false
  }]
}
