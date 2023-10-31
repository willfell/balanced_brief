import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import argparse
import time
import datetime
from datetime import datetime
import pytz

AWS_REGION = "us-west-1"
SLACK_CHANNEL = "#brief-logs"
SLACK_CHANNEL_ID = "C0632AXULTZ"
try:
    PIPELINE_NAME = os.environ['PIPELINE_NAME']
except:
    PIPELINE_NAME = "None"


# Initialize a Web API client
client = WebClient(token=os.environ["SLACK_TOKEN"])
if os.environ['EXECUTION_LOCATION'] != "LOCAL":
    task_execution_url = f"https://us-west-1.console.aws.amazon.com/ecs/v2/clusters/bf-cluster/tasks/{os.environ['AWS_TASK_ID']}/configuration?region=us-west-1&selectedContainer=bf-service"
else:
    task_execution_url = "https://us-west-1.console.aws.amazon.com/ecs/v2/clusters/bf-cluster/services?region=us-west-1"

def init_job_run_message():
    mountain_tz = pytz.timezone('America/Denver')
    now = datetime.now(mountain_tz)
    day_of_month = now.strftime('%d')
    month = now.strftime('%B')
    time_of_day = now.strftime('%H:%M %p')
    try:
            response = client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=f"Balanced Brief Job Execution",
                blocks=[
                    {
                        "type": "header",
                        "text": {
                                "type": "plain_text",
                                "text": f"Balanced Brief Job Started | {month} {day_of_month}"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text":  f"`{month} {day_of_month} {time_of_day} MT`"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Task Being Executed"
                            },
                            "url": task_execution_url,
                        }
                    }
                ])
            return response['ts']
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")
        return False
  
def progress_message(thread_ts, message):
  try:
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
  
def final_message_success(thread_ts):
  try:
      # Post a message to the channel and get the "thread_ts" value from the response
      response = client.chat_postMessage(
          channel=SLACK_CHANNEL,
          attachments=[
              {
                  "color": "good",  
                  "text": "Execution Successful"
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
  try:
      # Post a message to the channel and get the "thread_ts" value from the response
      message_text = message + "\n<@U010QGMM078>"
      response = client.chat_postMessage(
          channel=SLACK_CHANNEL,
          attachments=[
              {
                  "color": "#FF0000",  
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

def final_job_run_success(thread_ts):
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

def final_job_run_failure(thread_ts):
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--function_name', type=str, help='Name of the function to call')
    parser.add_argument('--thread_ts', type=str, default=None, required=False, help='Slack thread number')
    parser.add_argument('--message', type=str, default=None, required=False, help='The text used for the message')

    args = parser.parse_args()
    function_name = args.function_name
    thread_ts = args.thread_ts
    message = args.message

    if function_name == 'init_job_run_message':
        thread_ts = init_job_run_message()
        print(thread_ts)
    elif function_name == 'progress_message' and thread_ts:
        progress_message(thread_ts, message)
    elif function_name == 'final_message_success' and thread_ts:
        final_message_success(thread_ts)
    elif function_name == 'final_message_failure' and thread_ts:
        final_message_failure(thread_ts, message)
    elif function_name == 'final_job_run_success' and thread_ts:
        final_job_run_success(thread_ts)
    elif function_name == 'final_job_run_failure' and thread_ts:
        final_job_run_failure(thread_ts)
