#!/bin/bash

# set -x
set -e

set_variables() {
  cd $CODEBUILD_SRC_DIR
  export COMMIT_AUTHOR=$(git log -n 1 --pretty=format:'%an')
  export COMMIT=$(echo "$CODEBUILD_RESOLVED_SOURCE_VERSION" | cut -c 1-7)
  export BRANCH_NAME="$(git symbolic-ref HEAD --short 2>/dev/null)"
  if [ "$BRANCH_NAME" = "" ] ; then
    export BRANCH_NAME="$(git rev-parse HEAD | xargs git name-rev | cut -d' ' -f2 | sed 's/remotes\/origin\///g')";
  fi
  export SLACK="python3 $CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py"
}

set_variables

install_slack_dependencies() {
  echo "Installing Slack Dependencies"
  pip3 install -r "$CODEBUILD_SRC_DIR/Terraform/Slack/requirements.txt"
}

init_pipeline_message() {
  python3 "$CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py" --function_name=init_pipeline_message
}

init_build_message() {
  python3 "$CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py" --function_name=init_build_message 
}

final_message_failure() {
  local thread_ts="$1"
  local message="$2"
  $SLACK --function_name=final_message_failure --thread_ts=$thread_ts --message="$message"
}

final_message_success() {
  local thread_ts="$1"
  local message="$2"
  python3 "$CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py" --function_name=final_message_success --thread_ts=$thread_ts --message="$message"
}

progress_message() {
  local thread_ts="$1"
  local message="$2"
  python3 "$CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py" --function_name=progress_message --thread_ts=$thread_ts --message="$message"
}

determine_thread_id() {
  python3 "$CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py" --function_name=determine_slack_thread_id
}

upload_file() {
  local thread_ts="$1"
  local file_path="$2"
  python3 "$CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py" --function_name=upload_file --thread_ts=$thread_ts --file_path=$file_path
}

final_pipeline_update_success() {
  local thread_ts="$1"
  python3 "$CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py" --function_name=final_pipeline_update_success --thread_ts=$thread_ts
}

final_pipeline_update_failure() {
  local thread_ts="$1"
  python3 "$CODEBUILD_SRC_DIR/Terraform/Slack/slack_messenger.py" --function_name=final_pipeline_update_failure --thread_ts=$thread_ts
}


case "$1" in
  install_dependencies)
    install_slack_dependencies
    ;;
  set_vars)
    set_variables
    ;;
  init_pipeline_message)
    init_pipeline_message 
    ;;
  init_build_message)
    init_build_message 
    ;;
  final_message_failure)
    final_message_failure "$2" "$3"
    ;;
  final_message_success)
    final_message_success "$2" "$3"
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
  final_pipeline_update_success)
    final_pipeline_update_success "$2"
    ;;
  final_pipeline_update_failure)
    final_pipeline_update_failure "$2"
    ;;
  *)
    echo "Invalid command"
    exit 1
    ;;
esac