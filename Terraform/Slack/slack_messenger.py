import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import argparse
import time
import datetime



slack_token = os.environ["SLACK_API_TOKEN"]
git_commit_author = os.environ["COMMIT_AUTHOR"]
git_commit = os.environ["COMMIT"]
git_branch = os.environ["BRANCH_NAME"]
AWS_ACCOUNT = os.environ["AWS_ACCOUNT"]
CODE_BUILD_PROJECT_NAME = os.environ["CODE_BUILD_PROJECT_NAME"]
AWS_REGION = os.environ["AWS_REGION"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]
SLACK_CHANNEL_ID = os.environ['SLACK_CHANNEL_ID']
try:
    PIPELINE_NAME = os.environ['PIPELINE_NAME']
except:
    PIPELINE_NAME = "None"

# Tracking build time 
build_start_timestamp = float(os.environ['CODEBUILD_START_TIME']) / 1000  # Convert to seconds

# Initialize a Web API client
client = WebClient(token=slack_token)


slack_user_ids = {
    "118227376+ashishvpatel94@users.noreply.github.com": "@U04A7S3PSB0",
    "132947179+will-fellhoelter@users.noreply.github.com": "@U056GUR33BK",
    "92753277+mikaelapc@users.noreply.github.com": "@U02HZFPNKJN",
    "95256342+blakecannon-projectcanary@users.noreply.github.com": "@U02P4D37BFS",
    "blakecannon-projectcanary": "@U02P4D37BFS",
    "W. Blake Cannon": "@U02P4D37BFS",
    "ashish.patel@projectcanary.com": "@U04A7S3PSB0",
    "blake.cannon@projectcanary.com": "@U02P4D37BFS",
    "jon.gridley@gmail.com": "@U03CTC28MCY",
    "jon.gridley@projectcanary.com": "@U03CTC28MCY",
    "Jon Gridley": "@U03CTC28MCY",
    "jongridley": "@U03CTC28MCY",
    "kieran.lynn@github.com": "@U01TA8X8UCA",
    "kieran.lynn@projectcanary.com": "@U01TA8X8UCA",
    "mikaela.currier@projectcanary.com": "@U02HZFPNKJN",
    "mikaelapc": "@U02HZFPNKJN",
    "roman.gavrilov@gmail.com": "@U03GQPQCJKT",
    "roman.gavrilov@projectcanary.com": "@U03GQPQCJKT",
    "Roman": "@U03GQPQCJKT",
    "will.fellhoelter@projectcanary.com": "@U056GUR33BK",
    "Will Fellhoelter": "@U056GUR33BK",
    "will_fell": "@U056GUR33BK",
    "will-fellhoelter": "@U056GUR33BK"
}

initial_build_message = f"Build - <https://console.aws.amazon.com/codesuite/codebuild/{AWS_ACCOUNT}/projects/{CODE_BUILD_PROJECT_NAME}/history?region={AWS_REGION}|{CODE_BUILD_PROJECT_NAME.lower()}>\n`{git_commit}:{git_commit_author}`         `{git_branch}` "
initial_pipeline_message = f"Pipeline - <https://us-east-2.console.aws.amazon.com/codesuite/codepipeline/pipelines/{PIPELINE_NAME}/view?region={AWS_REGION}|{PIPELINE_NAME.lower()}>\n\n`{git_commit}:{git_commit_author}`         `{git_branch}`"
codebuild_project_url = f"https://console.aws.amazon.com/codesuite/codebuild/{AWS_ACCOUNT}/projects/{CODE_BUILD_PROJECT_NAME}/history?region={AWS_REGION}"
pipeline_project_url = f"https://us-east-2.console.aws.amazon.com/codesuite/codepipeline/pipelines/{PIPELINE_NAME}/view?region={AWS_REGION}"


def init_pipeline_message():
  try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=f"Pipeline Started - {PIPELINE_NAME.lower()}",
            blocks=[
                {
                    "type": "header",
                    "text": {
                            "type": "plain_text",
                            "text": f"Pipeline Started - {PIPELINE_NAME.lower()}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text":  f"`{git_commit}:{git_commit_author}`\n`{git_branch}`"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Pipeline"
                        },
                        "url": pipeline_project_url,
                    }
                }
            ])
        return response['ts']
  except SlackApiError as e:
      assert e.response["ok"] is False
      assert e.response["error"]
      print(f"Got an error: {e.response['error']}")
      return False


def init_build_message():
  thread_ts = determine_slack_thread_id()
  if not thread_ts:
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=f"Build Started - {CODE_BUILD_PROJECT_NAME.lower()}",
            blocks=[
                {
                    "type": "header",
                    "text": {
                            "type": "plain_text",
                            "text": f"Build Started - {CODE_BUILD_PROJECT_NAME.lower()}",
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text":  f"`{git_commit}:{git_commit_author}`\n`{git_branch}`"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Code Build Project"
                        },
                        "url": codebuild_project_url,
                    }
                }
            ])
        return response['ts']
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")
        return False
  else:
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            thread_ts=thread_ts,
            text=f"Build Started - {CODE_BUILD_PROJECT_NAME.lower()}",
            blocks=[
                {
                    "type": "header",
                    "text": {
                            "type": "plain_text",
                            "text": f"Build Started - {CODE_BUILD_PROJECT_NAME.lower()}",
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text":  f"`{git_commit}:{git_commit_author}`\n`{git_branch}`"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Code Build Project"
                        },
                        "url": codebuild_project_url,
                    }
                }
            ])
        return thread_ts
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")
  
def progress_message(thread_ts, message):
  try:
      print(f"Attempting to send message with {thread_ts}")
      response = client.chat_postMessage(
          channel=SLACK_CHANNEL,
          text=message,
          thread_ts=thread_ts
      )
  except SlackApiError as e:
      assert e.response["ok"] is False
      assert e.response["error"]
      print(f"Got an error: {e.response['error']}")
      print(f"The thread ts that you're trying to use is {thread_ts}")
      print(f"{e.response}")
      return False
  
def final_message_success(thread_ts, message):
  try:
      # Post a message to the channel and get the "thread_ts" value from the response
      message_text = initial_build_message + "\n" + message
      response = client.chat_postMessage(
          channel=SLACK_CHANNEL,
          attachments=[
              {
                  "color": "good",  
                  "text": message_text
              }
          ],
          thread_ts=str(thread_ts),
          reply_broadcast=False
      )
      return response.data["ts"]
  except SlackApiError as e:
      assert e.response["ok"] is False
      assert e.response["error"]
      print(f"Got an error: {e.response['error']}")
      return False
  
def final_message_failure(thread_ts, message):
  commit_author = determine_commit_author(git_commit_author)
  try:
      # Post a message to the channel and get the "thread_ts" value from the response
      message_text = initial_build_message + "\n" + message + "\n" + commit_author
      response = client.chat_postMessage(
          channel=SLACK_CHANNEL,
          attachments=[
              {
                  "color": "#FF0000",  
                  "text": message_text
              }
          ],
          thread_ts=str(thread_ts),
          reply_broadcast=True
      )
      return response.data["ts"]
  except SlackApiError as e:
      assert e.response["ok"] is False
      assert e.response["error"]
      print(f"Got an error: {e.response['error']}")
      return False

def final_pipeline_update_success(thread_ts):
    try:
        # Add the reaction to the specified message
        client.reactions_add(
            channel=SLACK_CHANNEL_ID,
            timestamp=thread_ts,
            text="Adding check mark",
            name="white_check_mark"
        )
    except SlackApiError as e:
        print(f"Error adding reaction: {e.response['error']}")

def final_pipeline_update_failure(thread_ts):
    try:
        # Add the reaction to the specified message
        client.reactions_add(
            channel=SLACK_CHANNEL_ID,
            timestamp=thread_ts,
            text="Adding x",
            name="x"
        )
    except SlackApiError as e:
        print(f"Error adding reaction: {e.response['error']}")


def upload_file(thread_ts, file_path):
  try:
      # Post a message to the channel and get the "thread_ts" value from the response
    with open(file_path, 'r') as file:
      data = json.load(file)
    response = client.chat_postMessage(
        channel=SLACK_CHANNEL,
        blocks=json.dumps(data['blocks']),
        attachments=data['attachments'],
        thread_ts=str(thread_ts),
        text="Infracost Report"
    )
    return response
  except SlackApiError as e:
      assert e.response["ok"] is False
      assert e.response["error"]
      print(f"Got an error: {e.response['error']}")
      return False


def determine_commit_author(git_commit_author):
  for name, slack_id in slack_user_ids.items():
      if name == git_commit_author:
          return f"<{slack_id}>"
  return "<!channel>"

def determine_slack_thread_id():
    # This Project doesn't require one slack thread for all tests, sending thread_ts as false unless it changes
    if 'ts' in os.environ:
        return os.environ['ts']
    thread_ts = False
    import json
    import datetime
    import pytz
    import time

    mst = pytz.timezone('US/Mountain')

    current_time_mst = datetime.datetime.now(mst)

    time_period_ago = current_time_mst - datetime.timedelta(seconds=3600)
    one_hour_ago = time_period_ago.timestamp()
    response = client.conversations_history(channel=SLACK_CHANNEL_ID, oldest=one_hour_ago)
    messages = response['messages']
    #print(json.dumps(messages, indent=4))
    #print("Determing thread id")
    #print(json.dumps(messages, indent=4))

    # Check for Pipeline Run First to find thread
    for message in messages:
        slack_event_timestamp = float(message['ts'])
        is_build_start_after_slack_event = build_start_timestamp > slack_event_timestamp
        if is_build_start_after_slack_event:
            if 'blocks' in message:
                for block in message['blocks']:
                    if block['type'] == 'header' and 'text' in block:
                        if PIPELINE_NAME.lower() in block['text']['text']:
                            return message['ts']
                    
    # If that didn't return anything, we search for anything matching the commit, author, and branch
    if not thread_ts:
        for message in messages:
            slack_event_timestamp = float(message['ts'])
            is_build_start_after_slack_event = build_start_timestamp > slack_event_timestamp
            if is_build_start_after_slack_event:
                if 'blocks' in message:  
                    for block in message['blocks']:
                        if block['type'] == "section" and 'text' in block:
                            if block['text']['text'] == f"`{git_commit}:{git_commit_author}`\n`{git_branch}`":
                                if slack_event_timestamp < build_start_timestamp:
                                    return message['ts']
    return thread_ts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--function_name', type=str, help='Name of the function to call')
    parser.add_argument('--thread_ts', type=str, default=None, required=False, help='Slack thread number')
    parser.add_argument('--message', type=str, default=None, required=False, help='The text used for the message')
    parser.add_argument('--file_path', type=str, default=None, required=False, help='File path to upload')

    args = parser.parse_args()
    function_name = args.function_name
    thread_ts = args.thread_ts
    message = args.message
    file_path = args.file_path

    if function_name == 'init_pipeline_message':
        thread_ts = init_pipeline_message()
        print(thread_ts)
    elif function_name == 'init_build_message':
        thread_ts = init_build_message()
        print(thread_ts)
    elif function_name == 'progress_message' and thread_ts:
        progress_message(thread_ts, message)
    elif function_name == 'final_message_success' and thread_ts:
        final_message_success(thread_ts, message)
    elif function_name == 'final_message_failure' and thread_ts:
        final_message_failure(thread_ts, message)
    elif function_name == 'determine_commit_author':
        author_slack_id = determine_commit_author()
        print(author_slack_id)
    elif function_name == 'upload_file':
        file_upload = upload_file(thread_ts, file_path)
        print(file_upload)
    elif function_name == 'final_pipeline_update_success' and thread_ts:
        final_pipeline_update_success(thread_ts)
    elif function_name == 'final_pipeline_update_failure' and thread_ts:
        final_pipeline_update_failure(thread_ts)
    elif function_name == 'determine_slack_thread_id':
        slack_thread_id = determine_slack_thread_id()
        print(slack_thread_id)

