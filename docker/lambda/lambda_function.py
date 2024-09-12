import sys
import importlib.util


def handler(event, context):
    crawler = event['crawler']
    args = event['args']

    print(f'crawler: {crawler}')
    print(f'args: {args}')


    spec = importlib.util.spec_from_file_location(f'crawlers.{crawler}.main', f'crawlers/{crawler}/main.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    response = module.main()

    if response:
        return {
            'statusCode': 200,
            'body': response
        }


    return {
        'statusCode': 500,
        'body': response
    }
