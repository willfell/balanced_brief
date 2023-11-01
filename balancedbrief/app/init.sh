#!/bin/sh

# Retrieve the config from AWS Secrets Manager
if [ "$EXECUTION_LOCATION" != "LOCAL" ]; then
    SECRET_NAME="bb/config"  
else
    SECRET_NAME="bb/config-local"
    export AWS_TASK_ARN="local"
fi

METADATA=$(curl $ECS_CONTAINER_METADATA_URI_V4)
echo "$METADATA"
AWS_TASK_ID=$(echo $METADATA | jq -r '.DockerId')
export AWS_TASK_ID  

config=$(aws secretsmanager get-secret-value --secret-id "$SECRET_NAME" --query 'SecretString' --output text)
while IFS="=" read -r key value; do
    export "$key=$value"
    echo "Exported: $key"
done < <(echo "$config" | jq -r 'to_entries | .[] | "\(.key)=\(.value)"')

function stop_instance() {
    $SLACK progress_message "$ts" "Stopping DB Instance"
    python3 /app/db/instance_state/stop.py
}

# Initiate Slack Message
SLACK="bash /app/slack/slack_setup.sh"
ts=$($SLACK init_job_run_message)
export ts


if [ "$EXECUTION_LOCATION" != "LOCAL" ]; then
    echo "======================================================================================"
    echo "======================================================================================"
    echo "Start DB"
    echo "======================================================================================"
    echo "======================================================================================"
    $SLACK progress_message "$ts" "Starting up DB Instance"
    python3 /app/db/instance_state/start.py
    if [ $? -ne 0 ]; then
        $SLACK final_message_failure "$ts" "Turning on DB Instance Failed"
        $SLACK final_job_run_failure "$ts"
        stop_instance
        exit 1
    else
        $SLACK progress_message "$ts" ":white_check_mark: Instance Successfully Started"
    fi

fi


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


echo "======================================================================================"
echo "======================================================================================"
echo "Running Article Scraping" 
echo "======================================================================================"
echo "======================================================================================"
$SLACK progress_message "$ts" "Scraping Articles"
python3 /app/article_scraping/scraping.py
if [ $? -ne 0 ]; then
    $SLACK final_message_failure "$ts" "Scraping Articles Failed"
    $SLACK final_job_run_failure "$ts"
    stop_instance
    exit 1
    else
        $SLACK progress_message "$ts" ":white_check_mark: Article Scraping Completed Successfully"
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
    stop_instance
    exit 1
    else
        $SLACK progress_message "$ts" ":white_check_mark: Email Template Creation and Sending Completed Successfully"
fi


if [ "$EXECUTION_LOCATION" != "LOCAL" ]; then
    stop_instance
    if [ $? -ne 0 ]; then
        $SLACK final_message_failure "$ts" "Stopping Instance Failed"
        $SLACK final_job_run_failure "$ts"
        stop_instance
        exit 1
        else
            $SLACK progress_message "$ts" ":white_check_mark: Instance Stopped Successfully"
            $SLACK final_message_success "$ts" "Job Ran Successfully"
            $SLACK final_job_run_success "$ts" 
    fi
else
    $SLACK final_message_success "$ts" "Job Ran Successfully"
    $SLACK final_job_run_success "$ts" 
fi
