data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

# data "external" "git_hash" {
#   program = ["bash", "${path.cwd}/Scripts/git-hash.sh"]
# }

data "aws_ecr_authorization_token" "token" {
  registry_id = data.aws_caller_identity.current.account_id
}

data "aws_secretsmanager_secret" "ssh_key" {
  name = "balanced_brief_ssh_key"
}

data "aws_secretsmanager_secret_version" "ssh_key" {
  secret_id = data.aws_secretsmanager_secret.ssh_key.id
}

data "aws_secretsmanager_secret" "db_pass" {
  name = "postgres_db_pass"
}

data "aws_secretsmanager_secret_version" "db_pass" {
  secret_id = data.aws_secretsmanager_secret.db_pass.id
}

data "aws_secretsmanager_secret" "local_ssh_key" {
  name = "will_fell_local_ssh"
}

data "aws_secretsmanager_secret_version" "local_ssh_key" {
  secret_id = data.aws_secretsmanager_secret.local_ssh_key.id
}

