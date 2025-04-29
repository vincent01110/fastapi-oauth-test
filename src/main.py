from fastapi import FastAPI
from .config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import urllib.parse
from fastapi.responses import RedirectResponse
import requests

params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "scope": "openid email profile",
    "access_type": "offline",
    "prompt": "consent"
}

app = FastAPI()

@app.get('/')
def hello():
    return 'Hello World'

@app.get('/auth/login')
def login():
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    
    return RedirectResponse(url)


@app.get("/auth/callback")
def auth_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    response = requests.post(token_url, data=data)
    token_data = response.json()
    
    
    print(token_data)
    
    access_token = token_data['access_token']
    
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    return {
        "access_token": access_token,
        "user": user_info
    }