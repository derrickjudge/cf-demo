output "vulnerable_app_name_servers" {
  description = "Cloudflare nameservers to set at the registrar for letmeshowthevalue.com"
  value       = module.vulnerable_app_zone.name_servers
}

output "vulnerable_app_d1_database_id" {
  description = "D1 database ID for the vulnerable-app Worker"
  value       = module.vulnerable_app_zone.d1_database_id
}

output "mtpcollective_name_servers" {
  description = "Cloudflare nameservers to set at Vercel (registrar) for mtpcollective.com"
  value       = module.mtpcollective_zone.name_servers
}
