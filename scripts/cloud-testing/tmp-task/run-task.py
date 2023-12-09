import boto3
import json
from datetime import datetime
import time


# Prompt for command being used
def run_command():
    print("-----------------------------")
    print("Running Task")

    fd = open(
        "config.json",
    )
    config = json.load(fd)
    account_id = config["account_id"]
    region = config["region"]
    task_arn = config["taskRoleArn"]
    execution_rule = config["execution_task_role_arn"]
    task_name = config["ecs_cluster"] + "-temporary-task"
    ecs_cluster = config["ecs_cluster"]
    ecs_service = config["ecs_service"]
    subnets = config["subnets"]
    security_group = config["security_group"]
    environment_vars = config["environment_vars"]
    log_group = config["log_group"]

    session = boto3.session.Session(region_name=config["region"])
    ec2 = session.resource("ec2")
    client = session.client("ecs")

    response = client.describe_services(
        cluster=ecs_cluster,
        services=ecs_service,
    )

    for i in response["services"]:
        task_used = i["taskDefinition"]

    response = client.describe_task_definition(
        taskDefinition=task_used,
    )

    # for i in response['taskDefinition']['containerDefinitions']:
    #     if i['logConfiguration']['options']['awslogs-stream-prefix'] == 'laravel':
    #         image_used = i['image']

    # if image_tag != None:

    # image_used = image_used.split(":")[0]+":"+image_tag
    # response = json.loads(response)
    image_used = response["taskDefinition"]["containerDefinitions"][0]["image"]
    print("Image used for task -", image_used)

    # Create Task Definition - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.register_task_definition
    response = client.register_task_definition(
        family=task_name,
        taskRoleArn=task_arn,
        executionRoleArn=execution_rule,
        networkMode="awsvpc",
        containerDefinitions=[
            {
                "name": "balanced-brief-tmp-task-py",
                "image": image_used,
                "cpu": 1024,
                "memory": 2048,
                "essential": True,
                "environment": environment_vars,
                "entryPoint": ["sh", "init.sh"],
                "disableNetworking": False,
                "portMappings": [
                    {"containerPort": 5432, "hostPort": 5432, "protocol": "tcp"}
                ],
                "privileged": False,
                "readonlyRootFilesystem": False,
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": log_group,
                        "awslogs-region": region,
                        "awslogs-stream-prefix": "bf",
                    },
                },
            },
        ],
        placementConstraints=[],
        requiresCompatibilities=[
            "FARGATE",
        ],
        cpu="1024",
        memory="2048",
        runtimePlatform = {
            "cpuArchitecture": "ARM64",
            "operatingSystemFamily": "LINUX",
        },
        tags=[
            {"key": "Name", "value": "Balanced Brief Temporary Task"},
        ],
    )

    # Run task
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.run_task
    revision = response["taskDefinition"]["revision"]
    task_def_to_run = task_name + ":" + str(revision)
    print("Task definition to be ran - ", task_def_to_run)
    print("-----------------------------")
    response = client.run_task(
        cluster=ecs_cluster,
        count=1,
        enableECSManagedTags=False,
        enableExecuteCommand=False,
        launchType="FARGATE",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": subnets,
                "securityGroups": security_group,
                "assignPublicIp": "DISABLED",
            }
        },
        startedBy="Manual Execution - Python",
        tags=[
            {"key": "Name", "value": "Temp Migrate Command"},
        ],
        taskDefinition=task_def_to_run,
    )

    arn = response["tasks"][0]["taskArn"]

    log_stream_name = "bf/balanced-brief-tmp-task-py/" + arn.split("/")[2]

    print("Logs")
    print("-----------------------------")

    log_client = session.client("logs")
    log_events = []
    exit_code = 0

    # Sleep loop to output logs while the task is running
    while True:
        time.sleep(5)
        response = client.describe_tasks(
            cluster=ecs_cluster,
            tasks=[
                arn,
            ],
        )
        if (
            response["tasks"][0]["lastStatus"] == "RUNNING"
            or response["tasks"][0]["lastStatus"] == "STOPPED"
        ):
            logs = log_client.get_log_events(
                logGroupName=log_group, logStreamName=log_stream_name
            )
            for event in logs["events"]:
                if event not in log_events:
                    print(
                        datetime.fromtimestamp(int(event["timestamp"]) / 1000).replace(
                            microsecond=0
                        ),
                        " -",
                        event["message"],
                    )
                    log_events.append(event)
        if response["tasks"][0]["lastStatus"] == "STOPPED":
            if "exitCode" not in response["tasks"][0]["containers"][0]:
                exit_code = 1
            elif response["tasks"][0]["containers"][0]["exitCode"] != 0:
                exit_code = 1
            break

    # Delete All of the Lingering Task Definitions
    client = session.client("ecs")
    print("-----------------------------")
    print("Deleting All Task Definitions")
    print("-----------------------------")
    response = client.list_task_definitions(familyPrefix=task_name)
    for task_def_arn in response["taskDefinitionArns"]:
        print(task_def_arn)
        client.deregister_task_definition(taskDefinition=task_def_arn)
    print("-----------------------------")
    if exit_code != 0:
        print("The Task had Problems and Exited in ERROR\n")
        exit(1)
    else:
        print("Task Complete\n")


if __name__ == "__main__":
    run_command()
