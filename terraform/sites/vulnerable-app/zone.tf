resource "cloudflare_zone" "this" {
  account = {
    id = var.account_id
  }
  name = "letmeshowthevalue.com"
  type = "full"
}
