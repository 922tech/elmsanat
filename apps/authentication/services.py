import requests
import json
from config import settings

client_id = settings.OAUTH_CREDENTIALS['login']['client_id']
client_secret = settings.OAUTH_CREDENTIALS['login']['client_secret']
token_url = settings.TOKEN_URL
revoke_token_url = settings.REVOKE_TOKEN_URL

class AuthService:

    @staticmethod
    def obtain_token_request(username, password):
        payload = json.dumps({
            "grant_type": "password",
            "client_id": client_id,
            "username": username,
            "password": password
            })
    
        response = requests.post(
            token_url,
            data=payload,
            auth=(client_id, client_secret),
        )
        return response
    
    @staticmethod
    def revoke_token_request(token):
        payload = json.dumps({
            "token": token,
            "client_id": client_id,
            "grant_type":"password",
            "client_secret": client_secret,
            
            })
    
        response = requests.post(
            revoke_token_url,
            data=payload,
        )
        return response
    

