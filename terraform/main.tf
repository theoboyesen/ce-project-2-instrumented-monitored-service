terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

data "aws_ami" "amazon_linux" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_security_group" "order_api_sg" {
  name        = "order-api-sg"
  description = "Security group for Order API service"

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Flask API"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "order_api_instance" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  key_name = aws_key_pair.observability_key.key_name

  vpc_security_group_ids = [aws_security_group.order_api_sg.id]

  tags = {
    Name = "order-api-instance"
  }
}

resource "aws_key_pair" "observability_key" {
  key_name   = "observability-key"
  public_key = file("observability-key.pub")
}