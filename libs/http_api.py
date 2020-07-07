'''Functions to call an http based API'''
import json
import requests

def restful_call(url: str, data: bool = False):  # data = 'json'
    '''make a request to a restful api'''
    #url = 'https://url'

    if isinstance(data, bool):
        return requests.post(url, headers={"Content-Type": "application/json"}).json()

    data_json = json.dumps(data, ensure_ascii=False)
    return requests.post(url, data=data_json, headers={"Content-Type": "application/json"}).json()
