import aiohttp
import webbrowser
import base64
from urllib.parse import urlencode
from typing import Optional


class YahooOAuth:
    """Handle Yahoo OAuth2 authentication without storing credentials."""
    
    AUTH_URL = "https://api.login.yahoo.com/oauth2/request_auth"
    TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
    REDIRECT_URI = "https://localhost/callback"
    
    def __init__(self, client_id: str, client_secret: str, user_email: Optional[str] = None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_email = user_email
        self._access_token = None
    
    async def authenticate(self) -> Optional[str]:
        """Perform OAuth2 authentication flow."""
        params = {
            'client_id': self._client_id,
            'redirect_uri': self.REDIRECT_URI,
            'response_type': 'code',
            'scope': 'openid',  # Basic scope - Fantasy permissions come from app settings
        }
        
        if self._user_email:
            params['login_hint'] = self._user_email
        
        auth_url = f"{self.AUTH_URL}?{urlencode(params)}"
        
        print("\n" + "=" * 60)
        print("AUTHORIZATION REQUIRED")
        print("=" * 60)
        print(f"\nOpening browser for Yahoo login...")
        print(f"\nIf browser doesn't open, copy this URL manually:")
        print(f"\n{auth_url}\n")
        print("=" * 60)
        
        webbrowser.open(auth_url)
        
        print("\n📋 After logging in and authorizing:")
        print("   1. Your browser will redirect to https://localhost/callback")
        print("   2. The page WON'T load - that's OK!")
        print("   3. Look at the URL bar, it will show:")
        print("      https://localhost/callback?code=XXXXXXXX")
        print("   4. Copy ONLY the code value (after 'code=')")
        print("")
        
        auth_code = input("Enter the authorization code from the URL: ").strip()
        
        if not auth_code:
            print("\n❌ No authorization code entered.")
            return None
        
        print("\n🔄 Exchanging code for access token...")
        
        self._access_token = await self._exchange_code(auth_code)
        return self._access_token
    
    async def _exchange_code(self, code: str) -> Optional[str]:
        """Exchange authorization code for access token."""
        credentials = f"{self._client_id}:{self._client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.REDIRECT_URI
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.TOKEN_URL, headers=headers, data=data) as response:
                    response_text = await response.text()
                    
                    if response.status == 200:
                        token_data = await response.json()
                        return token_data.get('access_token')
                    else:
                        print(f"\n❌ Token exchange failed!")
                        print(f"   Status: {response.status}")
                        print(f"   Response: {response_text}")
                        
                        if 'invalid_grant' in response_text:
                            print("\n   Hint: The authorization code may have expired. Try again.")
                        elif 'invalid_client' in response_text:
                            print("\n   Hint: Check your Client ID and Client Secret.")
                        
                        return None
        except Exception as e:
            print(f"\n❌ Error during token exchange: {e}")
            return None
    
    def clear_credentials(self):
        """Clear credentials from memory."""
        self._client_id = None
        self._client_secret = None
        self._user_email = None
        self._access_token = None