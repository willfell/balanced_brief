# ################################################################################
# # EC2
# ################################################################################


# // IAM for EC2 Resources
resource "aws_iam_role" "postgres" {
  name        = "${var.project_short_name}-db-instance-role"
  description = "Role for ${var.project_short_name} DB"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Sid = ""
      }
    ]
  })


  tags = merge(var.tags, { "Name" = var.project_short_name })


  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_iam_role_policy" "postgres_cloudwatch_agent" {
  name = "${var.project_short_name}-role-policy"
  role = aws_iam_role.postgres.id


  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "cloudwatch:PutMetricData",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams",
          "logs:DescribeLogGroups",
          "logs:CreateLogStream",
          "logs:CreateLogGroup",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Action = [
          "ssm:GetParameter",
          "ssm:PutParameter",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:ssm:*:*:parameter/AmazonCloudWatch-*"
      }
    ]
  })


  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_iam_role_policy_attachment" "postgres_secretsmanager" {
  role       = aws_iam_role.postgres.name
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"


  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_iam_role_policy_attachment" "postgres_ssm" {
  role       = aws_iam_role.postgres.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_iam_instance_profile" "postgres" {
  name = "${var.project_short_name}-pg-profile"
  role = aws_iam_role.postgres.name
}


# // EC2 Resources
resource "aws_instance" "db" {
  ami                         = var.instance_ami
  disable_api_termination     = true
  ebs_optimized               = false
  iam_instance_profile        = aws_iam_instance_profile.postgres.name
  instance_type               = "t4g.nano"
  key_name                    = var.ssh_key_name
  subnet_id                   = aws_subnet.private_subnet.id
  associate_public_ip_address = false
  vpc_security_group_ids      = [aws_security_group.allow_ssh.id]
  root_block_device {
    delete_on_termination = true
    encrypted             = false
    tags                  = merge(var.tags, { Name = "${var.project_short_name}-db-ROOT" })
    volume_size           = 20
  }
  tags = merge(var.tags, { Name = "${var.project_short_name}-db" })
  user_data = templatefile("${path.cwd}/templates/db-startup.sh", {
    DB_PASS       = data.aws_secretsmanager_secret_version.db_pass.secret_string
    LOCAL_SSH_KEY = data.aws_secretsmanager_secret_version.local_ssh_key.secret_string
  })


  lifecycle {
    ignore_changes = [
      # Ignore AMI and user_data in case of accidental changes that would cause attempted EC2 resource re-creation.
      ami,
      user_data,
    ]
  }
}

# resource "aws_instance" "bastion" {
#   ami                         = var.instance_ami
#   disable_api_termination     = true
#   ebs_optimized               = false
#   iam_instance_profile        = aws_iam_instance_profile.postgres.name
#   instance_type               = "t4g.nano"
#   key_name                    = var.ssh_key_name
#   subnet_id                   = aws_subnet.public_subnet.id
#   associate_public_ip_address = true
#   #security_groups = aws_security_group.allow_ssh.id
#   vpc_security_group_ids = [aws_security_group.allow_ssh.id]
#   root_block_device {
#     delete_on_termination = true
#     encrypted             = false
#     tags                  = merge(var.tags, { Name = "${var.project_short_name}-bastion-ROOT" })
#     volume_size           = 10
#   }
#   tags = merge(var.tags, { Name = "${var.project_short_name}-bastion" })
#   user_data = templatefile("${path.cwd}/templates/bastion-startup.sh", {
#     SSH_KEY = data.aws_secretsmanager_secret_version.ssh_key.secret_string
#     LOCAL_SSH_KEY = data.aws_secretsmanager_secret_version.local_ssh_key.secret_string
#   })



#   lifecycle {
#     ignore_changes = [
#       # Ignore AMI and user_data in case of accidental changes that would cause attempted EC2 resource re-creation.
#       ami,
#       user_data,
#     ]
#   }
# }
