output "name_servers" {
  description = "Cloudflare nameservers to set at the registrar for letmeshowthevalue.com"
  value       = cloudflare_zone.this.name_servers
}

output "d1_database_id" {
  description = "D1 database ID for the vulnerable-app Worker"
  value       = cloudflare_d1_database.vulnerable_app.id
}
