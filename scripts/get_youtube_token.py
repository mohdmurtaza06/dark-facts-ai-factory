from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
client_id = input("OAuth client ID: ").strip()
client_secret = input("OAuth client secret: ").strip()
config = {"installed": {
    "client_id": client_id, "client_secret": client_secret,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "redirect_uris": ["http://localhost"]
}}
flow = InstalledAppFlow.from_client_config(config, SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nAdd these as GitHub Actions secrets. Do not share them.\n")
print("YT_CLIENT_ID =", client_id)
print("YT_CLIENT_SECRET =", client_secret)
print("YT_REFRESH_TOKEN =", creds.refresh_token)
