resource "aws_security_group" "codebuild" {
  name        = "${local.name}-codebuild-sg"
  description = "Security group for the ${local.name} CodeBuild"
  vpc_id      = data.aws_vpc.main.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.cidr_private]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.cidr_private]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.cidr_public]
  }

  tags = merge(var.common_tags, tomap({ "Name" = "${local.name}-codebuild" }))
}
