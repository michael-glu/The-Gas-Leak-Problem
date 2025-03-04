from requests.api import request
import config
import requests

params = {
    "grant_type": "password",
    "client_id": config.client_id,
    "client_secret": config.client_secret,
    "username": config.username,
    "password": config.password
}
r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")
print("Access Token:", access_token)
print("Instance URL", instance_url)


def sf_api_call(action, parameters = {}, method = 'get', data = {}):
   """
   Helper function to make calls to Salesforce REST API.
   Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
   """
   headers = {
      'Content-type': 'application/json',
      'Accept-Encoding': 'gzip',
      'Authorization': 'Bearer %s' % access_token
   }
   if method in ['get', 'delete']:
      r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
   elif method in ['post', 'patch']:
      r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
   else:
      # other methods not implemented in this example
      raise ValueError('Method should be get or post or patch.')
   print('Debug: API %s call: %s' % (method, r.url) )
   if r.status_code < 300:
      if method in ['patch', 'delete']:
         return None
      else:
         return r.json()
   else:
      raise Exception('API error when calling %s : %s' % (r.url, r.content))


