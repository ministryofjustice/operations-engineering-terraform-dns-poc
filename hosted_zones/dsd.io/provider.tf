terraform {
  backend "s3" {
    bucket         = "dns-poc-terraform-state"
    key            = "terraform.tfstate"
    region         = "eu-west-2"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.9"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-2"
}
