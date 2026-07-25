terraform {
  required_version = ">= 1.9"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.0"
    }
  }

  # Remote state in R2 (S3-compatible API) — keeps state off local disk and
  # off any third-party service. access_key/secret_key are deliberately
  # omitted here: backend blocks can't reference variables, so they're
  # supplied at `terraform init` time via -backend-config flags (see
  # README) sourced from .env locally / GitHub secrets in CI. Never commit
  # real values here.
  #
  # State locking (`use_lockfile`) is left off: it depends on S3 conditional
  # writes (If-None-Match) that R2's docs don't explicitly confirm for plain
  # PutObject. Fine for a solo-operator poc demo with no concurrent applies —
  # revisit if this ever needs multi-operator locking.
  backend "s3" {
    bucket = "cf-demo-tfstate"
    key    = "cf-demo/terraform.tfstate"
    region = "auto"

    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
    use_path_style              = true

    endpoints = {
      s3 = "https://2d98f868fcca065a3813a2b6830bf477.r2.cloudflarestorage.com"
    }
  }
}

# api_token intentionally omitted — read from the CLOUDFLARE_API_TOKEN
# environment variable instead, so no secret ever lands in a committed file.
provider "cloudflare" {}
