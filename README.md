# A tool to update your public IP in AWS route53
If the public IP provided by your ISP is dynamic this will help you  
keep your domain A record (i.e example.com) updated.

## Important!
This tool needs to run from the network that has the public IP.  
It will use an external service to lookup the source IP and use that to update the record.

## Setup
The app requires environment variables to work.  
They are described in `env.example`

## Build
Build the docker image:  
`docker build --rm -f "Dockerfile" -t route53-record-updater:latest .`

## Run
To run it once:  
`docker run --env-file your-env-file route53-record-updater`

Since it doesn't start a running service this has to be scheduled (e.g cron) for continuous updates