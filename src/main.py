from fastapi import FastAPI
from .config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import urllib.parse
from fastapi.responses import RedirectResponse
import requests

params = {
    "client_id": CLIENT_ID,  # Client ID from the Google Cloud Auth Platform
    "redirect_uri": REDIRECT_URI, # Client Secret from the Google Cloud Auth Platform
    "response_type": "code", # Auth type, 'code' is prefered
    "scope": "openid email profile", # the date you need access to
    "access_type": "offline", # means that the google auth api also adds a refresh token
    "prompt": "consent" # show consent screen
}

app = FastAPI()

@app.get('/')
def hello():
    return 'Hello World'


# the client app fetches this endpoint which redirects to the google auth screen
@app.get('/auth/login')
def login():
    # embeds the params to the urls
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    
    # redirects client
    return RedirectResponse(url)

# this is where google will redirect the client after it logs in and gives consent
# the 'code' is nessecery to request additional resources, after consent google embeds
# it to the request params
@app.get("/auth/callback")
def auth_callback(code: str):
    # endpoint for requesting access tokens
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code, # the code that google provides after authentication
        "client_id": CLIENT_ID, # Client ID from the Google Cloud Auth Platform
        "client_secret": CLIENT_SECRET, # Client Secret from the Google Cloud Auth Platform
        "redirect_uri": REDIRECT_URI, # its the redirect uri that you provided on the Google Cloud Platform
        "grant_type": "authorization_code" # it tells the google api that you provide the 'code'
    }
    
    # requesting access token
    response = requests.post(token_url, data=data)
    token_data = response.json()
    
    print(token_data)
    
    access_token = token_data['access_token']
    
    # request definition
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # requesting profile information
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    return {
        "access_token": access_token,
        "user": user_info
    }