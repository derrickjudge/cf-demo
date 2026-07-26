resource "cloudflare_d1_database" "vulnerable_app" {
  account_id = var.account_id
  name       = "cf-demo-vulnerable-app-db"
}
