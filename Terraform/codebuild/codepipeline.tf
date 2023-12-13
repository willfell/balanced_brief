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
        ConnectionArn        = aws_codestarconnections_connection.codestar.arn
        FullRepositoryId     = "${var.github_organization}/${var.github_repository}"
        BranchName           = "fix/submit_to_db"
        OutputArtifactFormat = "CODEBUILD_CLONE_REF"
      }
    }
  }

  stage {
    name = "BackendDeploy"

    action {
      run_order        = 1
      name             = "BackendDeploy"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source"]
      output_artifacts = ["slack_thread_id"]
      version          = "1"

      configuration = {
        ProjectName   = aws_codebuild_project.backend_deploy.name
        PrimarySource = "source"
      }
    }
  }

stage {
  name = "Frontend"

  action {
    run_order        = 1
    name             = "FrontendDeploy"
    category         = "Build"
    owner            = "AWS"
    provider         = "CodeBuild"
    input_artifacts  = ["source", "slack_thread_id"]
    output_artifacts = []
    version          = "1"

    configuration = {
      ProjectName   = aws_codebuild_project.frontend_deploy.name
      PrimarySource = "source"
    }
  }
}

  tags = merge(var.common_tags, tomap({ "Name" = local.name }))
}

