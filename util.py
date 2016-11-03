#! /usr/bin/env python
import json


def fetch_credentials(file_name="credentials.json"):
    with open(file_name) as credentials:
        return json.load(credentials)
