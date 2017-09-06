# GitHub Releases Serverless Notifier

## Description
This is a set of simple AWS Lambda functions that are triggered by AWS Cloudwatch Scheduled events. 

The first functions purpose is to look at a specific, user defined github project's releases page and update a dynamodb table with the release information.

The second function is triggered daily to read the dynamodb table looking for new updates for any of the girhub projects and send a summary message to SNS, which in turn can be sent to email, Slack etc.

## Usage
```shell
#---------- TESTING ----------#
## Test the function using SAM Local CLI
make run function_name=NAME_OF_FUNCTION_TO_TEST event_type=TYPE_OF_EVENT_TO_USE_WITH_FUNCTION

#---------- DEPLOYING ----------#
# Package the function for deployment with Cloudformation
make package bucket_name=NAME_OF_S3_BUCKET bucket_prefix=NAME_OF_BUCKET_DIRECTORY

# Deploy the function using Cloudformation
make deploy bucket_name=NAME_OF_S3_BUCKET bucket_prefix=NAME_OF_BUCKET_DIRECTORY stack_name=NAME_TO_USE_FOR_CLOUDFORMATION_STACK
```

## Requirements
- [SAM Local CLI](https://github.com/awslabs/aws-sam-local)
- [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)

## License
MIT

