#!/bin/sh

# Retrieve the config from AWS Secrets Manager
if [ "$EXECUTION_LOCATION" != "LOCAL" ]; then
    SECRET_NAME="bb/config"  
else
    SECRET_NAME="bb/config-local"
    export AWS_TASK_ARN="local"
fi

METADATA=$(curl $ECS_CONTAINER_METADATA_URI_V4)
TASK_ID=$(echo $METADATA | jq -r '.DockerId | split("-")[0]')
TASK_SERVICE=$(echo $METADATA | jq -r '.DockerName')
export TASK_ID
export TASK_SERVICE

config=$(aws secretsmanager get-secret-value --secret-id "$SECRET_NAME" --query 'SecretString' --output text)
while IFS="=" read -r key value; do
    export "$key=$value"
    echo "Exported: $key"
done < <(echo "$config" | jq -r 'to_entries | .[] | "\(.key)=\(.value)"')

# Initiate Slack Message
SLACK="bash /app/slack/slack_setup.sh"
ts=$($SLACK init_job_run_message)
export ts


if [ "$EXECUTION_LOCATION" == "LOCAL" ]; then
    echo "======================================================================================"
    echo "======================================================================================"
    echo "Running Migrations"
    echo "======================================================================================"
    echo "======================================================================================"
    $SLACK progress_message "$ts" "Running Migrations"
    python3 /app/db/migrate.py
    if [ $? -ne 0 ]; then
        $SLACK final_message_failure "$ts" "Migrations Failed"
        $SLACK final_job_run_failure "$ts"
        stop_instance
        exit 1
        else
            $SLACK progress_message "$ts" ":white_check_mark: Migrations Completed Successfully"
    fi
fi

echo "======================================================================================"
echo "======================================================================================"
echo "Running Article Scraping" 
echo "======================================================================================"
echo "======================================================================================"
$SLACK progress_message "$ts" "Starting Article Scraping"
max_attempts=10
attempt=1
success=false

while [ $attempt -lt $max_attempts ]; do
    $SLACK progress_message "$ts" "Article Scraping Attempt #$attempt"
    python3 /app/article_scraping/scraping.py
    result=$?
    if [ $result -eq 0 ]; then
        success=true
        break
    else
        $SLACK progress_message "$ts" "Scraping Attempt failed"
        attempt=$((attempt+1))
        echo "Attempt $attempt of $max_attempts failed. Retrying..."
        sleep 5 
    fi
done

if [ $success = true ]; then
    $SLACK progress_message "$ts" ":white_check_mark: Article Scraping Completed Successfully"
else
    $SLACK final_message_failure "$ts" "Scraping Articles Failed after $max_attempts attempts"
    $SLACK final_job_run_failure "$ts"
    exit 1
fi


echo "======================================================================================"
echo "======================================================================================"
echo "Creating Email Templates and Sending" 
echo "======================================================================================"
echo "======================================================================================"
$SLACK progress_message "$ts" "Creating email templates and sending"
python3 /app/newsletter/create_email_template.py
if [ $? -ne 0 ]; then
    $SLACK final_message_failure "$ts" "Creating Email Templates Failed"
    $SLACK final_job_run_failure "$ts"
    exit 1
    else
        $SLACK progress_message "$ts" ":white_check_mark: Email Template Creation and Sending Completed Successfully"
        $SLACK final_message_success "$ts" "Job Ran Successfully"
        $SLACK final_job_run_success "$ts" 

fi


