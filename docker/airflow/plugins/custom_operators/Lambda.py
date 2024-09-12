import requests

def lambda_operator(function_name, args=None):
    url = "http://lambda:8080/2015-03-31/functions/function/invocations"
    function_payload = {
        'crawler': function_name,
        'args': args or {}
    }
    response = requests.post(url, json=function_payload)

    if response.status_code == 200:
        return response.json()

    raise Exception(response.text)
