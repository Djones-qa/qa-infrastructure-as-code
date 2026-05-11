output "selenium_hub_public_ip" {
  description = "Public IP of the Selenium Hub"
  value       = length(aws_instance.selenium_hub) > 0 ? aws_instance.selenium_hub[0].public_ip : null
}

output "selenium_hub_private_ip" {
  description = "Private IP of the Selenium Hub"
  value       = length(aws_instance.selenium_hub) > 0 ? aws_instance.selenium_hub[0].private_ip : null
}

output "selenium_node_public_ips" {
  description = "Public IPs of Selenium Nodes"
  value       = aws_instance.selenium_node[*].public_ip
}

output "test_runner_public_ip" {
  description = "Public IP of the test runner"
  value       = aws_instance.test_runner.public_ip
}

output "test_runner_instance_id" {
  description = "Instance ID of the test runner"
  value       = aws_instance.test_runner.id
}
