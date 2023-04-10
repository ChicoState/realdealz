import logging as log
from functools import wraps
from datetime import datetime as dt
import json
import urllib3
from environs import Env
import os

log.basicConfig(level=log.INFO)

def val_auth(func):
    '''For Validating Auth'''
    @wraps(func)
    def inner(self, *args, **kwargs):
        # check if url is in the arguments 
        if "url" in kwargs:
            url = kwargs["url"]
            if "igdb" in url:
                if dt.now().timestamp() - self.auth["request_time"] > self.auth["expires_in"]:
                    self.auth = self.get_auth_token()
        return func(self, *args, **kwargs)
    return inner



class Library:
    '''
    auth[id] - Client ID
    secret - Client Secret
    auth['Authorization'] - Auth token
    '''
    def __init__(self, load_credentials = False, on_init_authorize = False):
        log.info("initializing Library")
        self.base = {
            "steamspy": "steamspy.com/api.php?request=",
            "igdb": "https://api.igdb.com/v4/",
            "steam": "https://store.steampowered.com/api/",
        }
        self._id = None
        self._secret = None
        self.auth = None
        if load_credentials:
            self._load_cred()

        self.a_header = {"Client-ID": self._id}

        if on_init_authorize:
            self.auth = self.get_auth_token()
            self.a_header['Authorization'] = self.auth.pop('Authorization', None)
    
    def _load_cred(self):
        '''Loads the credentials from .env file if it exists'''
        if not os.path.exists('.env'):# if .env file exists  use it to load the credentials
            log.error("No .env file found")
            throw(Exception("No .env file found"))
            
        env = Env()
        env.read_env()
        self._secret = env.str("TWITCH_CLIENT_SECRET")
        self._id = env.str("TWITCH_CLIENT_ID")

        if not self._secret or not self._id:
            log.error("Client_secret or Client_id is not defined")
            throw(Exception("Client_secret or Client_id is not defined"))


    def get_auth_token(self):
        '''HTTP POST request to get twitch API auth token'''
        log.info("Getting auth token")
        http = urllib3.PoolManager()
        auth_url = "https://id.twitch.tv/oauth2/token"
        result = json.loads(http.request(
            'POST',
            auth_url,
            fields={"client_id": self._id, "client_secret": self._secret,
                     "grant_type": "client_credentials"}
        ).data)
        # clean the data
        result["request_time"] = dt.now().timestamp()
        result.pop('token_type', None)
        result['Authorization'] = 'Bearer' + " " + result.pop('access_token', None)
        if result['Authorization'] == " ":
            log.error('Could not get auth token')
        return result

    def search_all(self, content="mario asdf"):
        '''igdb API calls Game Slice'''
        _url = self.base['igdb'] + "search"
        _header = {
        }
        _fields = {
            "search": content,
            "fields": "*",
            "limit": 50,
        }
        return self.m_post(_url, _fields, _header)

    def get_top_100(self):
        '''Get the top 100 games in the last two weeks from steamspy'''
        _url = self.base['steamspy'] + "top100in2weeks"
        return self.m_get(_url, None)


    def m_get(self, url : str, p_headers : dict):
        '''Generic method for getting with twitch authentication'''
        http = urllib3.PoolManager()
        _headers = {
            "Content-Type": "application/json"
        }
        if p_headers is not None:
            _headers.update(p_headers)

        response = http.request('GET', url, headers=_headers)
        data = response.data
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        result = json.loads(data)

        #result = json.loads(http.request(
         #   'GET',
         #   url,
         #   headers=_headers
        #).data)
        return result


    @val_auth
    def m_post(self, url : str, p_fields : dict , p_headers : dict):
        '''Generic method for posting with twitch authentication'''
        http = urllib3.PoolManager()
        _headers = {
            "Content-Type": "application/json"
        }
        _headers.update(self.a_header)
        if p_headers is not None:
            _headers.update(p_headers)

        result = json.loads(http.request(
            'POST',
            url,
            headers=_headers,
            fields=p_fields
        ).data)
        return result

# This is for testing
# It will only run if this file is run directly
if __name__ == "__main__":
    library = Library(True, True)
    # print(library.search_all())
    # print(library.get_top_100())
