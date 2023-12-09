#!/bin/bash

# set -x
set -e

slack_executable="/app/slack/slack_messenger.py"
SLACK="python3 $slack_executable"

init_job_run_message() {
  $SLACK --function_name=init_job_run_message
}

final_message_failure() {
  local thread_ts="$1"
  local message="$2"
  $SLACK --function_name=final_message_failure --thread_ts=$thread_ts --message="$message"
}

final_message_success() {
  local thread_ts="$1"
  local message="$2"
  $SLACK --function_name=final_message_success --thread_ts=$thread_ts --message="$message"
}

progress_message() {
  local thread_ts="$1"
  local message="$2"
  $SLACK --function_name=progress_message --thread_ts=$thread_ts --message="$message"
}

final_job_run_success() {
  local thread_ts="$1"
  $SLACK --function_name=final_job_run_success --thread_ts=$thread_ts
}

final_job_run_failure() {
  local thread_ts="$1"
  $SLACK --function_name=final_job_run_failure --thread_ts=$thread_ts
}


case "$1" in
  init_job_run_message)
    init_job_run_message 
    ;;
  final_message_failure)
    final_message_failure "$2" "$3"
    ;;
  final_message_success)
    final_message_success "$2"
    ;;
  progress_message)
    progress_message "$2" "$3"
    ;;
  determine_thread_id)
    determine_thread_id
    ;;
  upload_file)
    upload_file "$2" "$3"
    ;;
  final_job_run_success)
    final_job_run_success "$2"
    ;;
  final_job_run_failure)
    final_job_run_failure "$2"
    ;;
  *)
    echo "Invalid command"
    exit 1
    ;;
esac