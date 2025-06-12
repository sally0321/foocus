from datetime import datetime
from dataclasses import asdict
import json
import requests

import pytds

from models.data import SessionMetrics

# CONN_STR = f"""Server=tcp:my-projects-svr.database.windows.net,1433;Initial Catalog=foocus;Persist Security Info=False;User ID=21058375@imail.sunway.edu.my;Password=19121819=toSLRS;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Authentication="Active Directory Password";"""

# DRIVER={ODBC Driver 17 for SQL Server};SERVER=my-projects-svr.database.windows.net;DATABASE=foocus;UID=21058375@imail.sunway.edu.my;PWD=19121819=toSLRS

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
    print(response.status_code)
    print(response.text)

