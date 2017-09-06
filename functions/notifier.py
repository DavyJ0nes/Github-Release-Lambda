from datetime import datetime, timedelta
import logging
import os
import boto3
from boto3.dynamodb.conditions import Attr
#  from botocore.exceptions import ClientError

# Getting Environment Variables
LOG_LEVEL = os.environ['LOG_LEVEL']
GH_INFO_TABLE = os.environ['GH_INFO_TABLE']
SNS_TOPIC = os.environ['SNS_TOPIC']

# Setting up logger
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Setting global boto3 resources
session = boto3.session.Session(region_name='eu-west-1')
dynamodb = session.resource('dynamodb')
sns = session.resource('sns')


def day_ago_epoch():
    logger.info("[day_ago_epoch]: Creating Epoch Timestamp")
    day_ago = datetime.now() - timedelta(hours=24)
    epoch = day_ago.strftime('%s')
    return epoch


def get_update_list(epoch):
    logger.info("[get_project_list]: Started")
    table = dynamodb.Table(GH_INFO_TABLE)
    fe = Attr('published_at_epoch').gt(int(epoch))

    response = table.scan(
        FilterExpression=fe,
    )

    update_list = []
    for r in response['Items']:
        update_list.append(r)

    return update_list


def format_update_message(updates):
    logger.info("[format_update_message]: Formatting Update Message")
    messages = []
    for update in updates:
        message = """
-----------------------------------------------------------------
Link: https://github.com/hashicorp/terraform/releases/tag/v0.10.1
Project: {}
New Version: {}

Link: {}""".format(update['project_name'],
                   update['tag_name'],
                   update['release_link']
                   )
        messages.append(message)

    return messages


def send_email(messages):
    logger.info("[send_email]: Sending Email")
    all_messages = "\n".join(messages)
    topic = sns.Topic(SNS_TOPIC)
    topic.publish(
        Message=all_messages,
        Subject="There is a new Release!"
    )


# lambda_handler is the main entry to this Lambda Function
def lambda_handler(event, context):
    # Starting
    logger.info("[lambda_handler]: Started")

    # Processing
    last_epoch = day_ago_epoch()
    updates = get_update_list(last_epoch)
    if len(updates) == 0:
        return "[lambda_handler]: No updates, exiting..."
    update_message = format_update_message(updates)
    send_email(update_message)

    # Complete
    return "[lambda_handler]: Complete"
