resource "cloudflare_d1_database" "vulnerable_app" {
  account_id = var.account_id
  name       = "cf-demo-vulnerable-app-db"

  # Explicit to match what Cloudflare actually set after creation --
  # leaving this unset makes Terraform try to PUT it back to null, which
  # the API rejects ("Expected object, received null").
  read_replication = {
    mode = "disabled"
  }
}
