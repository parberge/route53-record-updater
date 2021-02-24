[![Docker pulls](https://img.shields.io/docker/pulls/parberge/route53-record-updater.svg)](https://hub.docker.com/r/parberge/route53-record-updater)
[![actions](https://github.com/parberge/route53-record-updater/workflows/Python%20testing/badge.svg)](https://github.com/parberge/route53-record-updater/actions/workflows/main.yml)


# A tool to update your public IP in AWS route53
If the public IP provided by your ISP is dynamic this will help you  
keep your domain A record (i.e example.com) updated.

## Important!
This tool needs to run from the network that has the public IP.  
It will use an external service to lookup the source IP and use that to update the record.

It will also use [socket.gethostbyname](https://docs.python.org/3/library/socket.html#socket.gethostbyname) to check current resolved IP.

## Setup
The app requires environment variables to work.  
They are described in `env.example`

Credentials for AWS is required.
Provide the necessary env variables described here:  
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-environment-variables

You can find the route53 zone ID for your domain:
https://console.aws.amazon.com/route53/v2/hostedzones# and look for the `Hosted zone ID` column.


## Run
To run it once:  
`docker run --env-file your-env-file -e AWS_ACCESS_KEY_ID=foo -e AWS_SECRET_ACCESS_KEY=bar parberge/route53-record-updater:latest`

Since it doesn't start a running service this has to be scheduled (e.g cron) for continuous updates
