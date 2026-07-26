module "vulnerable_app_zone" {
  source     = "./sites/vulnerable-app"
  account_id = var.cloudflare_account_id
}
