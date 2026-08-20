terraform {
  required_version = ">= 1.12.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.2.0"
    }
    http    = { source = "hashicorp/http", version = ">= 3.4.2" }
    archive = { source = "hashicorp/archive", version = ">= 2.4.0" }
  }
}

provider "aws" {
  region = "us-east-1"
}