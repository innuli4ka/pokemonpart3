terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region     = var.region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  token      = var.aws_session_token
}

# Declare variables
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_session_token" {}
variable "region" {}
variable "ami" {}
variable "instance_type" {}
variable "key_name" {}

# Security Group
resource "aws_security_group" "pokemon_sg" {
  name_prefix = "pokemon-sg-"
  description = "Allow SSH, Flask API, Mongo (optional)"

  ingress {
    description = "SSH"
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

  ingress {
    description = "Mongo (optional)"
    from_port   = 27017
    to_port     = 27017
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instances
resource "aws_instance" "pokemon_game" {
  count                  = 2
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.pokemon_sg.id]

  tags = {
    Name = "pokemon-${count.index + 1}"
  }
}

# Output IPs
output "instance_public_ips" {
  value = [for instance in aws_instance.pokemon_game : instance.public_ip]
}
