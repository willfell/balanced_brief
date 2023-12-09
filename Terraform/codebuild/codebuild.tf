################################################################################
# CodeBuild
################################################################################

// CodeBuild Environment Variables
variable "terraform_version" {
  type        = string
  description = "The version of Hashicorp Terraform CodeBuild will install"
  default     = "1.5.5"
}

resource "aws_codebuild_project" "slack_init" {
  name          = "${local.name}-slack-init"
  build_timeout = 10
  service_role  = aws_iam_role.codebuild_role.arn
  description   = "Slack Init"

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:6.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true

    dynamic "environment_variable" {
      for_each = {
        SLACK_CHANNEL           = local.slack_integration.SLACK_CHANNEL
        SLACK_CHANNEL_ID        = local.slack_integration.SLACK_CHANNEL_ID
        SLACK_API_TOKEN         = local.slack_integration.SLACK_API_TOKEN
        PIPELINE_NAME           = local.name
        AWS_ACCOUNT             = data.aws_caller_identity.current.account_id
        CODE_BUILD_PROJECT_NAME = "${local.name}-slack-init"
        AWS_REGION              = data.aws_region.current.name
      }

      content {
        name  = environment_variable.key
        value = environment_variable.value
        type  = "PLAINTEXT"
      }
    }
  }



  source {
    type            = "CODEPIPELINE"
    location        = null
    git_clone_depth = null

    buildspec = templatefile("${path.cwd}/Templates/Buildspec/slack-init.yml.tftpl", {
      NAME = local.name
    })
  }

  vpc_config {
    vpc_id = data.aws_vpc.main.id

    subnets = [
      data.aws_subnet.private.id,
    ]

    security_group_ids = [
      aws_security_group.codebuild.id,
    ]
  }

  tags = merge(var.common_tags, tomap({ "Name" = "${local.name}-slack-init" }))
}

resource "aws_codebuild_project" "db_migrations" {
  name          = "${local.name}-database-migrations"
  build_timeout = 10
  service_role  = aws_iam_role.codebuild_role.arn
  description   = "Database Migrations"

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:6.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true

    dynamic "environment_variable" {
      for_each = {
        SLACK_CHANNEL           = local.slack_integration.SLACK_CHANNEL
        SLACK_CHANNEL_ID        = local.slack_integration.SLACK_CHANNEL_ID
        SLACK_API_TOKEN         = local.slack_integration.SLACK_API_TOKEN
        PIPELINE_NAME           = local.name
        AWS_ACCOUNT             = data.aws_caller_identity.current.account_id
        CODE_BUILD_PROJECT_NAME = "${local.name}-database-migrations"
        AWS_REGION              = data.aws_region.current.name
      }

      content {
        name  = environment_variable.key
        value = environment_variable.value
        type  = "PLAINTEXT"
      }
    }
  }



  source {
    type            = "CODEPIPELINE"
    location        = null
    git_clone_depth = null

    buildspec = templatefile("${path.cwd}/Templates/Buildspec/db-migrations.yml.tftpl", {
      NAME = local.name
    })
  }

  vpc_config {
    vpc_id = data.aws_vpc.main.id

    subnets = [
      data.aws_subnet.private.id,
    ]

    security_group_ids = [
      aws_security_group.codebuild.id,
    ]
  }

  tags = merge(var.common_tags, tomap({ "Name" = "${local.name}-slack-init" }))
}




# resource "aws_codebuild_project" "terraform_apply" {
#   name          = "${local.name}-terraform-apply"
#   build_timeout = 60
#   service_role  = aws_iam_role.codebuild_role.arn
#   description   = "Deploy via Terraform"

#   artifacts {
#     type = "CODEPIPELINE"
#   }

#   environment {
#     compute_type                = "BUILD_GENERAL1_MEDIUM"
#     image                       = "aws/codebuild/standard:6.0"
#     type                        = "LINUX_CONTAINER"
#     image_pull_credentials_type = "CODEBUILD"
#     privileged_mode             = true

#     dynamic "environment_variable" {
#       for_each = {
#         SLACK_CHANNEL           = local.slack_integration.SLACK_CHANNEL
#         SLACK_CHANNEL_ID        = local.slack_integration.SLACK_CHANNEL_ID
#         SLACK_API_TOKEN         = local.slack_integration.SLACK_API_TOKEN
#         NAME                    = local.name
#         AWS_ACCOUNT             = data.aws_caller_identity.current.account_id
#         CODE_BUILD_PROJECT_NAME = "${local.name}-terraform-apply"
#         PIPELINE_NAME           = local.name
#         AWS_REGION              = data.aws_region.current.name
#       }

#       content {
#         name  = environment_variable.key
#         type  = "PLAINTEXT"
#         value = environment_variable.value
#       }
#     }

#     dynamic "environment_variable" {
#       for_each = {
#         DB_PASSWORD       = "foo"
#         INFRACOST_API_KEY = "infracost-api-key"
#       }

#       content {
#         name  = environment_variable.key
#         type  = "PLAINTEXT"
#         value = environment_variable.value
#       }
#     }
#   }

#   source {
#     type = "CODEPIPELINE"
#     buildspec = templatefile("${path.cwd}/Templates/Buildspec/terraform-apply.yml.tftpl", {
#       BUCKET            = data.aws_s3_bucket.cicd_output.id
#       BUCKET_HTML       = lower("https://${data.aws_s3_bucket.cicd_output.bucket}")
#       DB_ENDPOINT       = "foo"
#       DB_NAME           = "foo"
#       ENVIRONMENT       = local.environment
#       NAME              = local.name
#       TERRAFORM_VERSION = var.terraform_version
#     })
#   }

#   vpc_config {
#     vpc_id = data.aws_vpc.main.id

#     subnets = [
#       data.aws_subnet.a_private.id,
#       data.aws_subnet.b_private.id,
#       data.aws_subnet.c_private.id,
#     ]

#     security_group_ids = [
#       aws_security_group.codebuild.id,
#     ]
#   }

#   tags = merge(local.common_tags, tomap({ "Name" = "${local.name}-terraform-apply" }))
# }
