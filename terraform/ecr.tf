resource "aws_ecr_repository" "repo" {
  name                 = "${var.project_short_name}-repo"
  image_tag_mutability = "MUTABLE"
  force_delete         = true


  image_scanning_configuration {
    scan_on_push = true
  }


  tags = merge(var.tags, { Name = "${var.project_short_name}-ecr-repo" })
}


resource "aws_ecr_lifecycle_policy" "policy" {
  repository = aws_ecr_repository.repo.name
  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep only last 2 images, expire all others."
        selection = {
          tagStatus   = "any"
          countType   = "imageCountMoreThan"
          countNumber = 2
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

locals {
  timestamp = formatdate("YYYYMMDDhhmmss", timestamp())
}


resource "docker_image" "image" {
  name = format("%v:%v", aws_ecr_repository.repo.repository_url, local.timestamp)
  build {
    context    = "${path.cwd}/../balancedbrief/app/"
    dockerfile = "Dockerfile"
    platform   = "linux/arm64"
  }
  lifecycle {
    create_before_destroy = true
  }

}


resource "docker_registry_image" "image" {
  name                 = docker_image.image.name
  insecure_skip_verify = true
  keep_remotely        = true
}
