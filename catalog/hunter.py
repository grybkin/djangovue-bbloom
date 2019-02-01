import requests
import json


def get_email_finder(domain, firstName, lastName):
    params = {'api_key': 'ea19db3bb7fdbd13bd97583d3543508df7e5801f',
            'domain': domain,
            'first_name': firstName,
            'last_name': lastName
    }

    res = requests.get('https://api.hunter.io/v2/email-finder', params=params)

    return json.loads(res.text)