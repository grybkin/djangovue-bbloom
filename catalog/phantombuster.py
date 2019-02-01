import requests
import json


def launch(companies, blacklist):

    params = {
        'companies': companies,
        'blacklist': blacklist,
    }
    headers = {'X-Phantombuster-Key-1': 'WSDECk7O7kdEgR67PnY4h47Cg4W3f52z'}

    res = requests.post('https://phantombuster.com/api/v1/agent/37962/launch', json=params, headers=headers)
    resText = res.text.encode('ascii','ignore')


    return json.loads(resText)