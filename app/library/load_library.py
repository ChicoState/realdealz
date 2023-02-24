from environs import Env
import datetime as dt
import urllib3
import json
import logging as log

log.basicConfig(level=log.INFO)

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
        print(self.auth)
        return
    
    # Decorator to check if auth token is expired
    def val_auth(self, func):
        def inner(*args, **kwargs):
            if dt.datetime.now().timestamp() - self.auth["request_time"] > self.auth["expires_in"]:
                self.auth = self.get_auth_token()
            return func(*args, **kwargs)
        return inner


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
        # Massage the data
        r["request_time"] = dt.datetime.now().timestamp()
        r['auth'] = r.pop('token_type', None) + " " + r.pop('access_token', None)
        if r['auth'] == " ":
            log.error('Could not get auth token')
        return r

    def get_game_slice(self):
        # HTTP GET request to get game slice
        log.info("Getting game slice")
        http = urllib3.PoolManager()
        gameSliceURL = "https://api.twitch.tv/helix/games/top"
        r = json.loads(http.request(
            'GET',
            gameSliceURL,
            headers={"Authorization": self.auth["auth"]}
        ).data)
        return r

if __name__ == "__main__":
    library = Library()
