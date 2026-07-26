output "vulnerable_app_name_servers" {
  description = "Cloudflare nameservers to set at the registrar for letmeshowthevalue.com"
  value       = module.vulnerable_app_zone.name_servers
}
