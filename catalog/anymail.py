import requests
import json


def get_email_finder(domain, firstName, lastName):
    params = {
            'domain': domain,
            'first_name': firstName,
            'last_name': lastName
    }
    headers = {'X-Api-Key': 'gmBZHtsrTMoEYSzuyZ7CTf5y'}

    res = requests.post('https://api.anymailfinder.com/v4.0/search/person.json', json=params, headers=headers)

    return json.loads(res.text)