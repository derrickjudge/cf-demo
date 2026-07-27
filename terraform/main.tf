module "vulnerable_app_zone" {
  source     = "./sites/vulnerable-app"
  account_id = var.cloudflare_account_id
}

module "mtpcollective_zone" {
  source     = "./sites/mtpcollective"
  account_id = var.cloudflare_account_id
}
