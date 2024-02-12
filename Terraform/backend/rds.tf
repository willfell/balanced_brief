################################################################################
# RDS
################################################################################
// Data Sources
resource "aws_db_subnet_group" "default" {
  name       = "bb-rds-subnet-group"
  subnet_ids = [aws_subnet.private_subnet.id, aws_subnet.public_subnet.id]

  tags = merge(var.tags, { "Name" = var.project_short_name })
}

data "aws_secretsmanager_secret" "db_password" {
  name = "bb/db/master-password"
}

data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = data.aws_secretsmanager_secret.db_password.id
}

// RDS Resources
resource "aws_kms_key" "bb_kms_rds_key" {
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  description              = "KMS key for Balanced Brief RDS cluster"
  deletion_window_in_days  = 7
  enable_key_rotation      = true
  is_enabled               = true
  key_usage                = "ENCRYPT_DECRYPT"
  multi_region             = false

  tags = merge(var.tags, { "Name" = var.project_short_name })
}

resource "aws_kms_alias" "bb_kms_rds_key_alias" {
  name          = "alias/bb_db_kms"
  target_key_id = aws_kms_key.bb_kms_rds_key.arn
}


resource "aws_db_instance" "bb_rds" {
  allocated_storage                   = 20
  db_name                             = "bbdb"
  engine                              = "postgres"
  engine_version                      = "15.5"
  instance_class                      = "db.t3.micro"
  username                            = "postgres"
  password                            = data.aws_secretsmanager_secret_version.db_password.secret_string
  skip_final_snapshot                 = false
  backup_retention_period             = 7
  db_subnet_group_name                = aws_db_subnet_group.default.id
  port                                = 5432
  vpc_security_group_ids              = [aws_security_group.rds.id]
  iam_database_authentication_enabled = false

}
