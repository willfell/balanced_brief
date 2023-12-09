data "aws_iam_policy_document" "codebuild_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["codebuild.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_iam_role" "codebuild_role" {
  name               = "${local.name}-codebuild-role"
  assume_role_policy = data.aws_iam_policy_document.codebuild_assume_role_policy.json
}

resource "aws_iam_role_policy" "codeartifact" {
  name = "${local.name}-codebuild-codeartifact"
  role = aws_iam_role.codebuild_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "codeartifact:DescribePackage",
          "codeartifact:DisassociateExternalConnection",
          "codeartifact:AssociateWithDownstreamRepository",
          "codeartifact:GetPackageVersionReadme",
          "codeartifact:PutRepositoryPermissionsPolicy",
          "codeartifact:ListTagsForResource",
          "codeartifact:DeletePackageVersions",
          "codeartifact:ListRepositoriesInDomain",
          "codeartifact:DescribePackageVersion",
          "codeartifact:GetDomainPermissionsPolicy",
          "codeartifact:ListDomains",
          "codeartifact:DisposePackageVersions",
          "codeartifact:ListPackageVersionDependencies",
          "codeartifact:TagResource",
          "codeartifact:GetAuthorizationToken",
          "codeartifact:ListPackages",
          "codeartifact:ReadFromRepository",
          "codeartifact:PutPackageOriginConfiguration",
          "codeartifact:GetPackageVersionAsset",
          "codeartifact:UntagResource",
          "codeartifact:CreateDomain",
          "codeartifact:DescribeRepository",
          "codeartifact:ListPackageVersionAssets",
          "codeartifact:DescribeDomain",
          "codeartifact:AssociateExternalConnection",
          "codeartifact:UpdateRepository",
          "codeartifact:CopyPackageVersions",
          "codeartifact:PutPackageMetadata",
          "codeartifact:ListRepositories",
          "codeartifact:UpdatePackageVersionsStatus",
          "codeartifact:GetRepositoryEndpoint",
          "codeartifact:CreateRepository",
          "codeartifact:PublishPackageVersion",
          "codeartifact:GetRepositoryPermissionsPolicy",
          "codeartifact:ListPackageVersions",
          "codeartifact:PutDomainPermissionsPolicy"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "sts:GetServiceBearerToken"
        Resource = "*"
        Condition = {
          StringEquals = {
            "sts:AWSServiceName" = "codeartifact.amazonaws.com"
          }
        }
      }
    ]
  })
}



data "aws_iam_policy_document" "codepipeline_assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["codepipeline.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_iam_role" "codepipeline_role" {
  name               = "${local.name}-codepipeline-role"
  assume_role_policy = data.aws_iam_policy_document.codepipeline_assume_role_policy.json
}

resource "aws_iam_role_policy" "codebuild_role_policy" {
  name = "${local.name}-codebuild-policy"
  role = aws_iam_role.codebuild_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
                "application-autoscaling:*",
                "rds:*",
                "firehose:*",
                "logs:*",
                "sqs:*",
                "autoscaling:*",
                "codebuild:*",
                "glue:*",
                "cognito-sync:*",
                "cloudfront:*",
                "secretsmanager:*",
                "ses:*",
                "kms:*",
                "wafv2:*",
                "codedeploy:*",
                "kinesis:*",
                "events:*",
                "sns:*",
                "cognito-identity:*",
                "s3:*",
                "chatbot:*",
                "codestar-notifications:*",
                "resource-groups:*",
                "cloudformation:*",
                "elasticloadbalancing:*",
                "codestar-connections:*",
                "iam:*",
                "elasticbeanstalk:*",
                "codecommit:*",
                "cloudwatch:*",
                "lambda:*",
                "route53:*",
                "ecs:*",
                "ec2:*",
                "ecr:*",
                "codepipeline:*",
                "cognito-idp:*",
                "acm:*",
                "sagemaker:*"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "codepipeline_role_policy" {
  name = "${local.name}-codepipeline-policy"
  role = aws_iam_role.codepipeline_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
                "application-autoscaling:*",
                "rds:*",
                "firehose:*",
                "logs:*",
                "sqs:*",
                "autoscaling:*",
                "codebuild:*",
                "glue:*",
                "cognito-sync:*",
                "cloudfront:*",
                "secretsmanager:*",
                "ses:*",
                "kms:*",
                "wafv2:*",
                "codedeploy:*",
                "kinesis:*",
                "events:*",
                "sns:*",
                "cognito-identity:*",
                "s3:*",
                "chatbot:*",
                "codestar-notifications:*",
                "resource-groups:*",
                "cloudformation:*",
                "elasticloadbalancing:*",
                "codestar-connections:*",
                "iam:*",
                "elasticbeanstalk:*",
                "codecommit:*",
                "cloudwatch:*",
                "lambda:*",
                "route53:*",
                "ecs:*",
                "ec2:*",
                "ecr:*",
                "codepipeline:*",
                "cognito-idp:*",
                "acm:*",
                "sagemaker:*"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}
