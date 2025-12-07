#!/usr/bin/env python3
"""
Helper script to get X (Twitter) OAuth2 User Context Bearer Token
Uses the 3-legged OAuth2 flow to authorize the app
"""

import os
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlencode, quote
from dotenv import load_dotenv
import time

load_dotenv()

class CallbackHandler(BaseHTTPRequestHandler):
    auth_code = None
    
    def do_GET(self):
        """Handle OAuth callback"""
        query_params = parse_qs(self.path.split('?')[1] if '?' in self.path else '')
        
        if 'code' in query_params:
            CallbackHandler.auth_code = query_params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """<html><body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>Authorization Successful!</h1>
            <p>You can close this window and return to the terminal.</p>
            </body></html>"""
            self.wfile.write(html.encode())
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress log messages

def get_user_bearer_token():
    """Get Bearer Token using OAuth2 3-legged User Context flow"""
    
    client_id = os.getenv('X_CLIENT_ID')
    client_secret = os.getenv('X_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Error: X_CLIENT_ID and X_CLIENT_SECRET not found in .env")
        return None
    
    print("🦊 X (Twitter) OAuth2 User Context Authorization\n")
    
    # Step 1: Generate authorization URL
    auth_url = "https://twitter.com/i/oauth2/authorize"
    redirect_uri = "http://localhost:8080/callback"
    
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "tweet.write tweet.read users.read",
        "state": "state",
        "code_challenge": "challenge",
        "code_challenge_method": "plain"
    }
    
    auth_url_full = f"{auth_url}?{urlencode(params)}"
    
    print("📱 Opening browser for authorization...")
    print(f"If browser doesn't open, visit: {auth_url_full}\n")
    
    # Open browser
    webbrowser.open(auth_url_full)
    
    # Start local server to receive callback
    print("⏳ Waiting for authorization...")
    server = HTTPServer(('localhost', 8080), CallbackHandler)
    
    # Wait for callback with timeout
    timeout = time.time() + 120  # 2 minutes timeout
    while CallbackHandler.auth_code is None and time.time() < timeout:
        server.handle_request()
    
    server.server_close()
    
    if not CallbackHandler.auth_code:
        print("❌ Authorization timeout or cancelled")
        return None
    
    auth_code = CallbackHandler.auth_code
    print(f"✅ Authorization code received!\n")
    
    # Step 2: Exchange code for access token
    print("🔄 Exchanging code for access token...")
    
    token_url = "https://api.twitter.com/2/oauth2/token"
    
    token_data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "code_verifier": "challenge",  # Must match code_challenge
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        
        token_response = response.json()
        bearer_token = token_response.get('access_token')
        
        if bearer_token:
            print("✅ Access Token obtained successfully!\n")
            print(f"🔐 Your Bearer Token:\n{bearer_token}\n")
            print("📝 Add this to your .env file as:")
            print(f"X_BEARER_TOKEN={bearer_token}\n")
            return bearer_token
        else:
            print("❌ No access token in response")
            print(f"Response: {token_response}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error exchanging code: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

if __name__ == "__main__":
    token = get_user_bearer_token()
    if token:
        print("✨ Token ready to use!")
    else:
        print("⚠️  Failed to get token. Please try again.")

