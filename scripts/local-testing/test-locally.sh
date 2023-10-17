#!/bin/bash

set -x
set -e

# Set the container name variable
CONTAINER_NAME=bb_test

# Specify the build context
CONTEXT_PATH=../../

# Specify the Dockerfile path
DOCKERFILE_PATH=$CONTEXT_PATH/balancedbrief/app/Dockerfile

# Start up the DB
cd $CONTEXT_PATH/db/docker
docker-compose up -d
sleep 3

# Change to the app directory - (Note: Be sure to verify this change is needed for your build)
cd $CONTEXT_PATH/balancedbrief/app

# Building the Docker image
docker build -t $CONTAINER_NAME -f $DOCKERFILE_PATH $CONTEXT_PATH

# Running the Docker container
docker run --network=docker_postgres \
           -e REDDITAGENT="$REDDITAGENT" \
           -e REDDITCLIENTSECRET="$REDDITCLIENTSECRET" \
           -e REDDITCLIENTID="$REDDITCLIENTID" \
           -e OPENAI_KEY="$OPENAI_KEY" \
           -e DB_PASS="$DB_PASS" \
           -e DB_HOST="postgres" \
           -e AWS_ACCESS_KEY_ID="$BB_ACCESS_KEY_ID" \
           -e AWS_SECRET_ACCESS_KEY="$BB_ACCESS_SECRET_KEY" \
           -e AWS_REGION="$BB_AWS_REGION" \
           -e ENV="$ENV" \
           -e EXECUTION_LOCATION="$EXECUTION_LOCATION" \
           $CONTAINER_NAME
