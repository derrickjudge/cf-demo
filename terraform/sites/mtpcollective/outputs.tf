output "name_servers" {
  description = "Cloudflare nameservers to set at Vercel (registrar) for mtpcollective.com"
  value       = cloudflare_zone.this.name_servers
}
