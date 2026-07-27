resource "cloudflare_zone_setting" "ssl_mode" {
  zone_id    = cloudflare_zone.this.id
  setting_id = "ssl"
  value      = "full"
}
