# aws-secretmanager-env
This is a python tool used to maintain secrets inside your containerized application
that is 
populate AWS Secret Manager key-values as environment variables.
Practical usage is to use side-by-side with the dockerized app without a need to 
build a new docker image and redeploy when passwords, tokens and etc expire.

It uses json-like string to identify ARN of the AWS Secrets Manager item and converts
it to the linux env file.

* Example 1:
  Secret's name: prod/my_service
  Command:
  ```bash
  > $ python3 secrets.py -n 'prod/my_service'
  ```

* Example 2:
  Secret's tags:
  ```yaml
   - environment: prod
   - service: my_service
  ```
  Command:
  ```bash
  > $ python3 secrets.py -t '{"environment": "prod", "service": "my_service"}'
  ```
  
  As the most reasonable way of usage is to put it inside the docker container you
  may want to install ```nuitka``` python package and compile it to the binary file
  with the ```build.sh``` script. 
