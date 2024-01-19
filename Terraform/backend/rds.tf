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

// Main Database
resource "aws_rds_cluster" "bb_rds" {

  allow_major_version_upgrade     = false
  apply_immediately               = true
  availability_zones              = ["us-west-1c"]
  backup_retention_period         = 5
  database_name                   = "bbdb"
  deletion_protection             = true
  copy_tags_to_snapshot           = true
  cluster_identifier              = "bbdbcluster"
  db_subnet_group_name            = aws_db_subnet_group.default.id
  enabled_cloudwatch_logs_exports = ["postgresql"]
  engine                          = "aurora-postgresql"
  engine_mode                     = "provisioned"
  engine_version                  = "14.3"
  final_snapshot_identifier       = "bb-db-snapshot"
  kms_key_id                      = aws_kms_alias.bb_kms_rds_key_alias.arn
  master_username                 = "postgres"
  master_password                 = data.aws_secretsmanager_secret_version.db_password.secret_string
  port                            = 5432
  preferred_backup_window         = "05:29-05:59"
  preferred_maintenance_window    = "tue:06:48-tue:07:18"
  skip_final_snapshot             = false
  storage_encrypted               = true
  vpc_security_group_ids          = [aws_security_group.rds.id]
  iam_database_authentication_enabled = false

  serverlessv2_scaling_configuration {
    max_capacity = 1.0                                     # 0.5 ACU = 1GB
    min_capacity = 0.5
  }

  lifecycle {
    ignore_changes = [
      engine_version, master_password, availability_zones, backtrack_window, cluster_members, kms_key_id
    ]
  }

}

resource "aws_rds_cluster_instance" "bb_rds" {

  availability_zone            = "us-west-1c"
  copy_tags_to_snapshot        = true
  cluster_identifier           = aws_rds_cluster.bb_rds.id
  engine                       = aws_rds_cluster.bb_rds.engine
  engine_version               = aws_rds_cluster.bb_rds.engine_version
  identifier                   = "bb-instance-1"
  instance_class               = "db.r6g.large"
  publicly_accessible          = false
  db_subnet_group_name         = aws_db_subnet_group.default.id
  preferred_maintenance_window = "tue:07:48-tue:08:18"

}

# // Integration Testing Database
# resource "aws_db_cluster_snapshot" "bb_rds_snapshot" {

#   db_cluster_identifier          = aws_rds_cluster.bb_rds.cluster_identifier
#   db_cluster_snapshot_identifier = lower(replace("${local.name}-db-init", "dev", "test"))
# }
