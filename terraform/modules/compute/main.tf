data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "selenium_hub" {
  count         = var.selenium_hub_count
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = var.public_subnet_ids[0]

  vpc_security_group_ids = [
    aws_security_group.selenium_hub.id
  ]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
    encrypted   = true
  }

  user_data = base64encode(templatefile("${path.module}/templates/selenium-hub-init.sh", {
    environment = var.environment
  }))

  tags = {
    Name = "qa-${var.environment}-selenium-hub-${count.index + 1}"
    Role = "selenium-hub"
  }
}

resource "aws_instance" "selenium_node" {
  count         = var.selenium_node_count
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = var.public_subnet_ids[count.index % length(var.public_subnet_ids)]

  vpc_security_group_ids = [
    aws_security_group.selenium_node.id
  ]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
    encrypted   = true
  }

  user_data = base64encode(templatefile("${path.module}/templates/selenium-node-init.sh", {
    environment = var.environment
    hub_host    = aws_instance.selenium_hub[0].private_ip
  }))

  tags = {
    Name = "qa-${var.environment}-selenium-node-${count.index + 1}"
    Role = "selenium-node"
  }

  depends_on = [aws_instance.selenium_hub]
}

resource "aws_instance" "test_runner" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = var.public_subnet_ids[0]

  vpc_security_group_ids = [
    aws_security_group.test_runner.id
  ]

  root_block_device {
    volume_size = 50
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name = "qa-${var.environment}-test-runner"
    Role = "test-runner"
  }
}

resource "aws_security_group" "selenium_hub" {
  name        = "qa-${var.environment}-selenium-hub-sg"
  description = "Security group for Selenium Hub"
  vpc_id      = var.vpc_id

  ingress {
    description = "Selenium Grid UI and API"
    from_port   = 4444
    to_port     = 4444
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "qa-${var.environment}-selenium-hub-sg"
  }
}

resource "aws_security_group" "selenium_node" {
  name        = "qa-${var.environment}-selenium-node-sg"
  description = "Security group for Selenium Nodes"
  vpc_id      = var.vpc_id

  ingress {
    description     = "Node communication from Hub"
    from_port       = 5555
    to_port         = 5555
    protocol        = "tcp"
    security_groups = [aws_security_group.selenium_hub.id]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "qa-${var.environment}-selenium-node-sg"
  }
}

resource "aws_security_group" "test_runner" {
  name        = "qa-${var.environment}-test-runner-sg"
  description = "Security group for test runner"
  vpc_id      = var.vpc_id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "qa-${var.environment}-test-runner-sg"
  }
}
