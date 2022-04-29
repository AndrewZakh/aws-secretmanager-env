'''
This module is used to create an env file containing AWS
Secrets Manager secrets that were obtained by name or tags.
Output is the .env file.
'''
import logging
from json import loads as json_loads
from argparse import ArgumentParser as arg_parser
from boto3.session import Session as boto_ssn

logging.basicConfig(level=logging.INFO,
                    # encoding='utf-8',
                    format='%(asctime)s %(name)s'
                    ' - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logs = logging.getLogger('secrets')


def create_filters(filter_string, filter_type):
    '''Compose an aws filter list of dictionaries.'''
    my_filters = []
    if filter_type == 'tags':
        filter_dict = json_loads(filter_string)
        for key, value in filter_dict.items():
            my_filters.append({'Key': 'tag-key', 'Values': [key]})
            my_filters.append({'Key': 'tag-value', 'Values': [value]})
    elif filter_type == 'name':
        my_filters.append({'Key': 'name', 'Values': [filter_string]})
    return my_filters


def main(filters):
    '''Convert secrets to env variables.'''
    session = boto_ssn()
    aws = session.client(service_name='secretsmanager')
    my_secrets = aws.list_secrets(Filters=filters)
    if len(my_secrets['SecretList']) == 1:
        arn = my_secrets['SecretList'][0]['ARN']
        logs.info(f'AWS secrets manager storage has been found: { arn }')
        my_values = aws.get_secret_value(SecretId=arn)
        env_dict = json_loads(my_values['SecretString'])
        with open('./.env', 'w') as svc_env:
            for env_var, env_val in env_dict.items():
                svc_env.write(f'export { env_var }="{ env_val }"\n')
    elif len(my_secrets['SecretList']) == 0:
        logs.error(f'No secrets have been found! Filters used: { filters }')
    else:
        arns_list = []
        for secret in my_secrets['SecretList']:
            arns_list.append(secret['ARN'])
        print(f'Multiple secrets found: { arns_list }')


if __name__ == '__main__':
    parser = arg_parser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--tags',
                       help='JSON string with tags {key:value}')
    group.add_argument('-n', '--name',
                       help='Identify secret by friedly name')
    args = parser.parse_args()
    if args.tags is not None:
        my_filter = create_filters(args.tags, 'tags')
    elif args.name is not None:
        my_filter = create_filters(args.name, 'name')
    logs.info(f'Filters {my_filter}')
    main(my_filter)
