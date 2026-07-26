resource "cloudflare_workers_custom_domain" "vulnerable_app" {
  account_id = var.account_id
  zone_id    = cloudflare_zone.this.id
  hostname   = "letmeshowthevalue.com"
  service    = "cf-demo-vulnerable-app"
}
