# Terraform
################################################################################
terraform {
  required_version = ">= 1.5.5"


  backend "s3" {
    bucket = "balanced-brief-terraform-state"
    key    = "balanced-brief.tfstate"
    region = "us-west-1"
  }


  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>4.0"
    }

    docker = {
      source  = "kreuzwerker/docker"
      version = ">= 3.0"
    }


  }
}


provider "aws" {
  region = "us-west-1"
}

provider "docker" {
  registry_auth {
    address  = format("%v.dkr.ecr.%v.amazonaws.com", data.aws_caller_identity.current.account_id, data.aws_region.current.name)
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}
