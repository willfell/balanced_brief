# Terraform
################################################################################
terraform {
  required_version = ">= 1.5.5"


  backend "s3" {
    bucket = "balanced-brief-terraform-state"
    key    = "balanced-brief-frontend.tfstate"
    region = "us-west-1"
  }


  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>4.0"
    }
  }
}


provider "aws" {
  region = "us-west-1"
}

provider "aws" {
  region = "us-east-1"
  alias  = "useast1"
}
