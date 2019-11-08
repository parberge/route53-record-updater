# A tool to update DNS record in AWS

## Setup
The app requires environment variables to work.  
They are described in `env.example`

## Build
Build the docker image:  
`docker build --rm -f "Dockerfile" -t route53-record-updater:latest .`

## Run
To run it once:  
`docker run --env-file your-env-file route53-record-updater`

Since it doesn't start a running service this has to be scheduled (e.g cron) for continous updates