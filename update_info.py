import datetime
import json
import logging
import os
import urllib2
import boto3
#  from botocore.exceptions import ClientError

# Getting Environment Variables
ORG = os.environ['ORG']
PROJECT = os.environ['PROJECT']
LOG_LEVEL = os.environ['LOG_LEVEL']
GH_INFO_TABLE = os.environ['GH_INFO_TABLE']

# Setting up logger
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Setting global boto3 resources
session = boto3.session.Session(region_name='eu-west-1')
dynamodb = session.resource('dynamodb')

# Setting base url
base_url = 'https://api.github.com/repos'


# convert_timestamp_to_epoch takes datestring and returns epoch as Integer
def convert_timestamp_to_epoch(timestamp):
    logger.info("[convert_timestamp_to_epoch]: Creating Epoch Timestamp")
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    epoch = dt.strftime('%s')
    return int(epoch)


# get_release_info makes HTTP request to Github API and returns release info
def get_release_info(url):
    logger.info("[get_release_info]: Getting Release Info from %s" % url)
    info_raw = urllib2.urlopen(url).read()
    info_json = json.loads(info_raw)
    output = []
    for entry in info_json:
        epoch_ts = convert_timestamp_to_epoch(entry['published_at'])
        output.append({
            'id': entry['id'],
            'published_at': entry['published_at'],
            'published_at_epoch': epoch_ts,
            'tag_name': entry['tag_name'],
            'author': entry['author']['login'],
            'release_link': entry['html_url']
        })
    return output


def update_table(data, project_name):
    logger.info(
        "[update_table]: Updating Table with {} new entries".format(len(data)))
    table = dynamodb.Table(GH_INFO_TABLE)
    for entry in data:
        table.put_item(
            Item={
                'id': entry['id'],
                'project_name': project_name,
                'published_at': entry['published_at'],
                'published_at_epoch': entry['published_at_epoch'],
                'tag_name': entry['tag_name'],
                'author': entry['author'],
                'release_link': entry['release_link']
            }
        )
    logger.info("[update_table]: Updating Table with new info")
    return True


# lambda_handler is the main entry to this Lambda Function
def lambda_handler(event, context):
    # Starting
    logger.info("[lambda_handler]: Started")
    project = "{}/{}".format(ORG, PROJECT)
    url = "{}/{}/releases".format(base_url, project)
    results = get_release_info(url)
    update_table(results, project)

    # Complete
    return "[lambda_handler]: Complete"
