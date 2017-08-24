# GitHub Releases Notifiero

## Description
This is a set of simple AWS Lambda functions that are triggered by AWS Cloudwatch Scheduled events. 

The first functions purpose is to look at a specific, user defined github project's releases page and update a dynamodb table with the release information.

The second function is triggered daily to read the dynamodb table looking for new updates for any of the girhub projects and send a summary message to SNS, which in turn can be sent to email, Slack etc.

## License
MIT

