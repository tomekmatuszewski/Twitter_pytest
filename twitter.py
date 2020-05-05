import re
import json
from urllib.parse import urljoin
import requests

USERS_API = "https://api.github.com/users/"


class Twitter:

    version = '1.0'

    def __init__(self, backend=None, username=None):
        self._tweets = []
        self.backend = backend
        self.username = username


    @property
    def tweets(self):
        if self.backend and not self._tweets:
            backend_text = self.backend.read()
            if backend_text:
                self._tweets = json.loads(backend_text)
        return self._tweets

    @property
    def tweet_messages(self):
        return [tweet['message'] for tweet in self.tweets]

    def get_user_avatar(self):
        if not self.username:
            return None
        url = urljoin(USERS_API, self.username)
        resp = requests.get(url)
        return resp.json()["avatar_url"]

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("Message to long.")
        self.tweets.append({'message': message, 'avatar': self.get_user_avatar()})
        if self.backend:
            self.backend.write(json.dumps(self.tweets))

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall("#(\w+) ?", message)]


if __name__ == '__main__':
    twitter = Twitter(username="python")
    twitter.tweet('test')
    print(twitter.tweets)




