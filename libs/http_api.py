"""Functions to call an http based API"""
import requests

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json;charset=utf-8",
    "User-Agent": "tackem/0.0.1",
}


def get(url: str, **params: dict) -> dict:
    """get with url creation"""
    r = requests.get(url, params=params, headers=HEADERS)
    r.raise_for_status()
    return r.json()


def post(url: str, **data: dict) -> dict:
    """get with url creation"""
    r = requests.post(url, data=data, headers=HEADERS)
    r.raise_for_status()
    return r.json()
