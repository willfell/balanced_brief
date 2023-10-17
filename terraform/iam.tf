resource "aws_iam_role" "role" { # this is the "execution role" for the ecs tasks
  assume_role_policy    = data.aws_iam_policy_document.policy.json
  force_detach_policies = true

  tags = merge(var.tags, { Name = "${var.project_short_name}-execution-role" })
}

data "aws_iam_policy_document" "policy" { # this is that execution role's assumption policy
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"
      identifiers = [
        "ec2.amazonaws.com",
        "ecs-tasks.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role_policy_attachment" "attachment_one" { # this allows the execution role to access ECR
  role       = aws_iam_role.role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}

resource "aws_iam_role_policy_attachment" "attachment_two" { # this allows the execution role to setup logging
  role       = aws_iam_role.role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

data "aws_iam_policy_document" "ecs_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"
      identifiers = [
        "ecs-tasks.amazonaws.com"
      ]
    }
  }
}


resource "aws_iam_role" "app_task_role" {
  assume_role_policy    = data.aws_iam_policy_document.ecs_assume_role.json
  force_detach_policies = true

  tags = merge(var.tags, { Name = "${var.project_short_name}-task-role" })
}


resource "aws_iam_role_policy_attachment" "app_task_role" {
  role       = aws_iam_role.app_task_role.name
  policy_arn = aws_iam_policy.task_role_policy.arn
}

# # Allows for the following:
# # # SES access
# # # S3:* for public and non public laravel buckets
# # # S3:*Object for request logs bucket
resource "aws_iam_policy" "task_role_policy" {
  description = "Policy for Role linked to API Task Definition"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ses:SendEmail",
          "ses:SendTemplatedEmail",
          "ses:SendCustomVerificationEmail",
          "ses:SendRawEmail",
          "ses:SendBulkTemplatedEmail",
          "ses:SendBounce",
          "ses:VerifyDomainDkim",
          "ses:VerifyEmailIdentity",
          "ses:VerifyDomainIdentity",
          "ses:GetIdentityVerificationAttributes"
        ],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "ec2:StartInstances",
          "ec2:StopInstances",
          "ec2:DescribeInstances",
          "ec2:DescribeInstanceStatus"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "scheduled_task_cloudwatch" {
  name = "scheduled-task-cloudwatch-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "events.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "scheduled_task_cloudwatch" {
  role = aws_iam_role.scheduled_task_cloudwatch.name
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ecs:*",
          "ec2:*",
          "iam:PassRole"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}
