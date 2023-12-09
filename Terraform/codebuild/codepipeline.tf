################################################################################
# CodePipeline
################################################################################

// CodePipeline Resources
resource "aws_codestarconnections_connection" "codestar" {
  name          = local.name
  provider_type = "GitHub"

  tags = merge(var.common_tags, tomap({ "Name" = local.name }))
}

resource "aws_codepipeline" "pipeline" {
  name     = local.name
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = data.aws_s3_bucket.artifacts_codepipeline.id
    type     = "S3"
  }

  stage {
    name = "Checkout"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      output_artifacts = ["source"]
      version          = "1"

      configuration = {
        ConnectionArn    = aws_codestarconnections_connection.codestar.arn
        FullRepositoryId = "${var.github_organization}/${var.github_repository}"
        BranchName           = "feature/user_sign_up"
        OutputArtifactFormat = "CODEBUILD_CLONE_REF"
      }
    }
  }
  stage {
    name = "SlackInit"

    action {
      run_order        = 1
      name             = "SlackInit"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source"]
      output_artifacts = ["slack_thread_id"]
      version          = "1"

      configuration = {
        ProjectName = aws_codebuild_project.slack_init.name
      }
    }
  }



  stage {
    name = "DBMigrations"

    action {
      run_order        = 2
      name             = "DBMigrations"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source", "slack_thread_id"]
      output_artifacts = []
      version          = "1"

      configuration = {
        ProjectName = aws_codebuild_project.db_migrations.name
        PrimarySource = "source"  
      }
    }
  }

  tags = merge(var.common_tags, tomap({ "Name" = local.name }))
}

// Slack Notifications
# resource "aws_codestarnotifications_notification_rule" "codepipeline" {
#   count = var.environment_terratest == false ? 1 : 0

#   detail_type = "BASIC"
#   event_type_ids = [
#     "codepipeline-pipeline-pipeline-execution-failed",
#     "codepipeline-pipeline-pipeline-execution-canceled",
#     "codepipeline-pipeline-pipeline-execution-started",
#     "codepipeline-pipeline-pipeline-execution-resumed",
#     "codepipeline-pipeline-pipeline-execution-succeeded",
#     "codepipeline-pipeline-pipeline-execution-superseded",
#     "codepipeline-pipeline-manual-approval-failed",
#     "codepipeline-pipeline-manual-approval-succeeded"
#   ]
#   name     = "${local.name}-codepipeline"
#   resource = aws_codepipeline.pipeline.arn

#   target {
#     address = "arn:aws:chatbot::${data.aws_caller_identity.current.account_id}:chat-configuration/slack-channel/all-${var.service}-codepipeline"
#     type    = "AWSChatbotSlack"
#   }
# }

# resource "aws_codestarnotifications_notification_rule" "codepipeline_failures_notifications" {
#   count = var.environment_terratest == false && local.environment == "prod" ? 1 : 0

#   detail_type = "BASIC"
#   event_type_ids = [
#     "codepipeline-pipeline-manual-approval-needed",
#     "codepipeline-pipeline-pipeline-execution-succeeded"
#   ]
#   name     = "${local.name}-approvals-failures"
#   resource = aws_codepipeline.pipeline.arn

#   target {
#     address = "arn:aws:chatbot::${data.aws_caller_identity.current.account_id}:chat-configuration/slack-channel/all-${var.service}-approvals-failures"
#     type    = "AWSChatbotSlack"
#   }
# }
