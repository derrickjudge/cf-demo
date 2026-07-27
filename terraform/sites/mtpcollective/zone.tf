resource "cloudflare_zone" "this" {
  account = {
    id = var.account_id
  }
  name = "mtpcollective.com"
  type = "full"
}
