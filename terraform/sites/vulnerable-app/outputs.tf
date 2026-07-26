output "name_servers" {
  description = "Cloudflare nameservers to set at the registrar for letmeshowthevalue.com"
  value       = cloudflare_zone.this.name_servers
}
