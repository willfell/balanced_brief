#!/bin/bash

set -x

# Logging function for easier and more readable logs
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Variables
FAMILY_PREFIX="bf"
SORT_ORDER="DESC"
MAX_ITEMS=1
CLUSTER_ARN="arn:aws:ecs:us-west-1:634560051830:cluster/bf-cluster"
LAUNCH_TYPE="FARGATE"
COUNT=1
SUBNETS="subnet-074bd5ec2ceb654dc"
#SUBNETS="subnet-0c290d1d60e82c401"
SECURITY_GROUPS="sg-0eb19f3ed5d53a04b"
ASSIGN_PUBLIC_IP="DISABLED"
STARTED_BY="CLI"

log "Fetching the latest task definition for family prefix: $FAMILY_PREFIX..."
LATEST_TASK_DEFINITION=$(aws ecs list-task-definitions --family-prefix $FAMILY_PREFIX --sort $SORT_ORDER --max-items $MAX_ITEMS --query "taskDefinitionArns[0]" --output text | head -n 1)

# If LATEST_TASK_DEFINITION is not empty, run the task with the latest definition
if [[ -n "$LATEST_TASK_DEFINITION" ]]; then
    # Extract the revision number
    REVISION=$(echo $LATEST_TASK_DEFINITION | awk -F ':' '{print $NF}')
    log "Found latest revision: $REVISION for family prefix: $FAMILY_PREFIX"

    log "Starting ECS task with revision: $REVISION..."
    aws ecs run-task \
      --cluster $CLUSTER_ARN \
      --launch-type $LAUNCH_TYPE \
      --task-definition $FAMILY_PREFIX:$REVISION \
      --count $COUNT \
      --network-configuration "awsvpcConfiguration={subnets=[$SUBNETS],securityGroups=[$SECURITY_GROUPS],assignPublicIp=$ASSIGN_PUBLIC_IP}" \
      --started-by $STARTED_BY \
      --overrides '{
          "containerOverrides": [{
              "name": "bf-task",
              "environment": [{
                  "name": "ENV",
                  "value": "TEST"
              }]
          }]
      }'

    if [[ $? -eq 0 ]]; then
        log "Successfully started ECS task with revision: $REVISION"
    else
        log "Error starting ECS task with revision: $REVISION"
    fi

else
    log "Failed to find the latest task definition for family prefix: $FAMILY_PREFIX."
fi
