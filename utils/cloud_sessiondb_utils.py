from dataclasses import asdict
import json
import requests
import os

from models.data import SessionMetrics

def insert_session_to_cloud_db(session_metrics: SessionMetrics):
    URL = f"{os.getenv("URL")}/insert-session"

    SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")

    headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }

    # Convert the dataclass object to a dictionary for JSON serialization
    body = asdict(session_metrics)

    # Send a POST request to the API
    response = requests.post(url=URL, headers=headers, json=body)

    # Return the response parsed as a Python dictionary
    return json.loads(response.text)

def get_weekly_top5_attention_span():
    URL = f"{os.getenv("URL")}/weekly-top5-attention-span"

    SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")

    headers = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }

    # Send a GET request to the API
    response = requests.get(url=URL, headers=headers)

    # Return the response parsed as a Python dictionary
    return json.loads(response.text)
