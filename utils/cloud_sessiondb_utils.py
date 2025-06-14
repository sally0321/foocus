from datetime import datetime
from dataclasses import asdict
import json
import requests

from models.data import SessionMetrics

server = 'my-projects-svr.database.windows.net'
database = 'foocus'
username = '21058375@imail.sunway.edu.my'
password = '19121819=toSLRS'

def insert_session_to_cloud_db(session_metrics: SessionMetrics):
    URL = "https://foocus-apim.azure-api.net/foocus/insert-session-metrics"

    SUBSCRIPTION_KEY = "34942be976114df393e1e2e7db7ea322"

    headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }

    body = asdict(session_metrics)

    response = requests.post(url=URL, headers=headers, json=body)
    return json.loads(response.text)

def get_weekly_top5_attention_span():
    URL = "https://foocus-apim.azure-api.net/foocus/weekly-top5-attention-span"

    SUBSCRIPTION_KEY = "34942be976114df393e1e2e7db7ea322"

    headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }

    response = requests.get(url=URL, headers=headers)
    return json.loads(response.text)
