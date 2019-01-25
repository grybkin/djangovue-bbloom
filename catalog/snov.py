import requests
import json


access_token = None

def get_access_token():
    global access_token

    if access_token:
        return access_token

    params = {
        'grant_type':'client_credentials',
        'client_id':'4188dafca07379d11005f87a613c370b',
        'client_secret': '7158b8357017dc892816f5d441b72c4a'
    }

    res = requests.post('https://app.snov.io/oauth/access_token', data=params)
    resText = res.text.encode('ascii','ignore')


    # response will be like this
    #bxXvDsQhR4TduWjOqaEOtQwSpd6Fafe4xwrilmV1

    access_token = json.loads(resText)['access_token']
    return access_token

def get_email_finder(domain, firstName, lastName):
    token = get_access_token()
    params = {'access_token':token,
            'domain': domain,
            'firstName': firstName,
            'lastName': lastName
    }

    res = requests.post('https://app.snov.io/restapi/get-emails-from-names', data=params)

    # response will be like this
    #{u'status': {u'identifier': u'complete', u'description': u'Emails search is completed'},
    # u'data': {u'lastName': u'vanrooyen', u'emails': [{u'email': u'gavin-vanrooyen@octagon.com', u'emailStatus': u'not_valid'}], u'firstName': u'gavin'},
    # u'params': {u'access_token': u'R2zDbvza563UVSsddsHfHhNHpMShU9exw70clLIE', u'lastName': u'vanrooyen', u'domain': u'octagon.com', u'firstName': u'gavin'}}

    return json.loads(res.text)