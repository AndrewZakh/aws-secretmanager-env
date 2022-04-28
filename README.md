# aws-secretmanager-env
Python tool to populate AWS Secret Manager key-values as environment variables.
Practical usage is to use side-by-side with the dockerized app without a need to 
build a new docker image and redeploy when passwords, tokens and etc expire.

It uses json-like string to identify ARN of the AWS Secrets Manager item and converts
it to the linux env file.
