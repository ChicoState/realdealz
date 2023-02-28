from environs import Env
from datetime import datetime as dt
import urllib3
import json
import logging as log
from functools import wraps

log.basicConfig(level=log.INFO)

"""_summary_
    Decorator to check if auth token is expired
"""
def val_auth(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if dt.now().timestamp() - self.auth["request_time"] > self.auth["expires_in"]:
            self.auth = self.get_auth_token()
        return func(self, *args, **kwargs)
    return inner



# 
"""
    # auth[id] - Client ID
    # secret - Client Secret
    # auth['Authorization'] - Auth token
"""
class Library: 
    def __init__(self, load = True):
        log.info("initializing Library")
        if not load: return 
        env = Env()
        env.read_env()
        self.secret = env.str("Client_secret")
        self.id = env.str("Client_id")
        if not self.secret or not self.id:
            log.error("Client_secret or Client_id is not defined") 
        self.auth = self.get_auth_token()
        self.a_header = {"Client-ID": self.id}
        self.a_header['Authorization'] = self.auth.pop('Authorization', None)
        return

    """
        Twitch API calls Authentication
    """
    def get_auth_token(self):
        # HTTP POST request to get auth token
        log.info("Getting auth token")
        http = urllib3.PoolManager()
        authURL = "https://id.twitch.tv/oauth2/token"
        r = json.loads(http.request(
            'POST',
            authURL,
            fields={"client_id": self.id, "client_secret": self.secret, "grant_type": "client_credentials"}
        ).data)
        # clean the data
        r["request_time"] = dt.now().timestamp()
        r.pop('token_type', None)
        r['Authorization'] = 'Bearer' + " " + r.pop('access_token', None)
        if r['Authorization'] == " ":
            log.error('Could not get auth token')
        return r

    # Twitch API calls Game Slice
    def search_all(self, content="mario asdf"):
        _url = "https://api.igdb.com/v4/search"
        _header = {
        }
        _fields = {
            "search": content,
            "fields": "*",
            "limit": 50,
        }
        return self.m_post(_url, _fields, _header)
        
    @val_auth
    def m_post(self, url, p_fields={}, p_headers={}):
        http = urllib3.PoolManager()
        _headers = {
            "Content-Type": "application/json"
        }
        _headers.update(self.a_header)
        _headers.update(p_headers)
        r = json.loads(http.request(
            'POST',
            url,
            headers=_headers,
            fields=p_fields
        ).data)
        return r

if __name__ == "__main__":
    library = Library()
    print(library.search_all())
