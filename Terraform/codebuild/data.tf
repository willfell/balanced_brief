data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_secretsmanager_secret" "slack_token" {
  name = "bb/slack-token"
}

data "aws_secretsmanager_secret_version" "slack_token" {
  secret_id = data.aws_secretsmanager_secret.slack_token.id
}

data "aws_subnet" "private" {
  vpc_id            = data.aws_vpc.main.id
  availability_zone = "us-west-1c"
  filter {
    name   = "tag:project"
    values = ["BalancedBrief"]
  }
}

data "aws_vpc" "main" {
  filter {
    name   = "tag:project"
    values = ["BalancedBrief"]
  }
}

data "aws_s3_bucket" "artifacts_codepipeline" {
  bucket = "balanced-brief-codepipeline"
}
