#!/bin/bash

set -x
set -e

# Set the container name variable
CONTAINER_NAME=bb_test

cd ../balancedbrief/app

docker build -t $CONTAINER_NAME .

docker run --network=scripts_postgres \
           -e REDDITAGENT="$REDDITAGENT" \
           -e REDDITCLIENTSECRET="$REDDITCLIENTSECRET" \
           -e REDDITCLIENTID="$REDDITCLIENTID" \
           -e OPENAI_KEY="$OPENAI_KEY" \
           -e DB_PASS="$DB_PASS" \
           -e DB_HOST="$DB_HOST" \
           -e AWS_ACCESS_KEY_ID="$BB_ACCESS_KEY_ID" \
           -e AWS_SECRET_ACCESS_KEY="$BB_ACCESS_SECRET_KEY" \
           -e AWS_REGION="$BB_AWS_REGION" \
           $CONTAINER_NAME
