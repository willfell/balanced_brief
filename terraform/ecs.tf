
resource "aws_ecs_cluster" "main" {
  name = "${var.project_short_name}-cluster"
  tags = merge(var.tags, { Name = "${var.project_short_name}-ecs-cluster" })
}

resource "aws_ecs_task_definition" "task_def" {
  family = var.project_short_name
  container_definitions = templatefile("${path.cwd}/task-definitions/db-service.json", {
    REDDITCLIENTID     = data.aws_secretsmanager_secret_version.reddit_client_id.secret_string
    REDDITCLIENTSECRET = data.aws_secretsmanager_secret_version.reddit_client_secret.secret_string
    REDDITAGENT        = data.aws_secretsmanager_secret_version.reddit_user_agent.secret_string
    OPENAI_KEY         = data.aws_secretsmanager_secret_version.open_ai_key.secret_string
    DB_PASS            = data.aws_secretsmanager_secret_version.db_pass.secret_string
    DB_HOST            = data.aws_secretsmanager_secret_version.db_host.secret_string
    IMAGE              = docker_registry_image.image.name
    NAME               = "${var.project_short_name}-task"
    LOGGROUP           = aws_cloudwatch_log_group.logs.name
    LOGPREFIX          = var.project_short_name
    REGION             = data.aws_region.current.name
  })
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  task_role_arn            = aws_iam_role.app_task_role.arn
  execution_role_arn       = aws_iam_role.role.arn
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }
  tags = merge(var.tags, { Name = "${var.project_short_name}-ecs-task-definition" })
}

resource "aws_cloudwatch_log_group" "logs" {
  name = "/aws/ecs/${var.project_short_name}-logs"
  tags = merge(var.tags, { Name = "${var.project_short_name}-ecs-log-group" })
}

resource "aws_ecs_service" "main" {
  name            = "${var.project_short_name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.task_def.arn
  desired_count   = 0
  launch_type     = "FARGATE"
  network_configuration {
    security_groups = [aws_security_group.ecs_tasks.id]
    subnets         = [aws_subnet.private_subnet.id]
  }
  tags = merge(var.tags, { Name = "${var.project_short_name}-ecs-service" })
}

resource "aws_cloudwatch_event_rule" "scheduled_task" {
  name                = "scheduled-ecs-event-rule"
  schedule_expression = "cron(0 12 * * ? *)"
}

resource "aws_cloudwatch_event_target" "scheduled_task" {
  target_id = "scheduled-ecs-target"
  rule      = aws_cloudwatch_event_rule.scheduled_task.name
  arn       = aws_ecs_cluster.main.arn
  role_arn  = aws_iam_role.scheduled_task_cloudwatch.arn

  ecs_target {
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.task_def.arn
    launch_type         = "FARGATE"
    network_configuration {
      subnets          = [aws_subnet.private_subnet.id]
      assign_public_ip = false
      security_groups  = [aws_security_group.ecs_tasks.id]
    }
  }
}
