################################################################################
# CodeBuild
################################################################################

// CodeBuild Environment Variables
variable "terraform_version" {
  type        = string
  description = "The version of Hashicorp Terraform CodeBuild will install"
  default     = "1.5.5"
}

resource "aws_codebuild_project" "backend_deploy" {
  name          = "${local.name}-backend-deploy"
  build_timeout = 10
  service_role  = aws_iam_role.codebuild_role.arn
  description   = "Backend Deploy"

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
        CODE_BUILD_PROJECT_NAME = "${local.name}-backend-deploy"
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

    buildspec = templatefile("${path.cwd}/Templates/Buildspec/backend-deploy.yml.tftpl", {
      NAME              = local.name
      TERRAFORM_VERSION = var.terraform_version
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



  tags = merge(var.common_tags, tomap({ "Name" = "${local.name}-backend-deploy" }))
}

resource "aws_codebuild_project" "frontend_deploy" {
  name          = "${local.name}-frontend-deploy"
  build_timeout = 10
  service_role  = aws_iam_role.codebuild_role.arn
  description   = "Frontend Deploy"

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
        CODE_BUILD_PROJECT_NAME = "${local.name}-frontend-deploy"
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

    buildspec = templatefile("${path.cwd}/Templates/Buildspec/frontend-deploy.yml.tftpl", {
      NAME              = local.name
      TERRAFORM_VERSION = var.terraform_version
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
}

