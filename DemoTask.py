import requests
import pandas as pd
import json


token_url = "https://login.microsoftonline.com/1b16ab3e-b8f6-4fe3-9f3e-2db7fe549f6a/oauth2/v2.0/token"

token_payload = 'grant_type=client_credentials&scope=api%3A%2F%2F7df8990a-8ce4-4092-885e-065faa6af062%2F.default'
token_headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Basic N2RmODk5MGEtOGNlNC00MDkyLTg4NWUtMDY1ZmFhNmFmMDYyOk41UDhRfjQ2dndJUy4tLldsVE5EVFZoRGN3M3BaSnNWaGlDaXdkeWk=',
  'Cookie': 'fpc=Av1shZQg_q1CvMY5yPQhXsAzPxrZAQAAABAz0N0OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
}

access_token =requests.request("GET", token_url, headers=token_headers, data=token_payload).json().get('access_token')
data = {
    'value': [access_token]
}

inputDF = pd.DataFrame(data)

data_url = "https://hexagon.onestreamcloud.com/OneStreamApi/api/DataProvider/GetAdoDataSetForSqlCommand?api-version=5.2.0"
print('token: ' ,access_token)

data_payload = json.dumps({
  "BaseWebServerUrl": "https://hexagon.onestreamcloud.com/OneStreamWeb",
  "ApplicationName": "Hexagon",
  "SqlQuery": "SELECT TOP 100 * FROM OS_MI_EXPORT_DATATABLE",
  "ResultDataTableName": "OS_MI_EXPORT_DATATABLE"
})
data_headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {inputDF["value"].iloc[0]}'
}



response = requests.request("POST", data_url, headers=data_headers, data=data_payload).json()
print(response)
outputDF = pd.DataFrame(response['OS_MI_EXPORT_DATATABLE'])