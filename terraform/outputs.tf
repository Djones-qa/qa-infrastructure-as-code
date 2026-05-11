output "vpc_id" {
  description = "ID of the VPC"
  value       = module.networking.vpc_id
}

output "selenium_hub_public_ip" {
  description = "Public IP of the Selenium Hub"
  value       = module.compute.selenium_hub_public_ip
}

output "selenium_hub_url" {
  description = "URL to access Selenium Grid console"
  value       = "http://${module.compute.selenium_hub_public_ip}:4444/ui"
}

output "test_runner_public_ip" {
  description = "Public IP of the test runner instance"
  value       = module.compute.test_runner_public_ip
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = module.database.rds_endpoint
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = module.database.rds_port
}
