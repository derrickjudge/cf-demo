resource "cloudflare_dns_record" "apex_a" {
  for_each = toset(["64.29.17.1", "216.198.79.1"])
  zone_id  = cloudflare_zone.this.id
  name     = "@"
  type     = "A"
  content  = each.value
  ttl      = 1
  proxied  = true
}

resource "cloudflare_dns_record" "www_cname" {
  zone_id = cloudflare_zone.this.id
  name    = "www"
  type    = "CNAME"
  content = "cname.vercel-dns.com"
  ttl     = 1
  proxied = true
}

resource "cloudflare_dns_record" "mx" {
  for_each = { "mx.zoho.com" = 10, "mx2.zoho.com" = 20, "mx3.zoho.com" = 50 }
  zone_id  = cloudflare_zone.this.id
  name     = "@"
  type     = "MX"
  content  = each.key
  priority = each.value
  ttl      = 1
}

resource "cloudflare_dns_record" "spf" {
  zone_id = cloudflare_zone.this.id
  name    = "@"
  type    = "TXT"
  content = "v=spf1 include:zohomail.com ~all"
  ttl     = 1
}

resource "cloudflare_dns_record" "zoho_verification" {
  zone_id = cloudflare_zone.this.id
  name    = "@"
  type    = "TXT"
  content = "zoho-verification=zb71659848.zmverify.zoho.com"
  ttl     = 1
}
