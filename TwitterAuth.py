from requests_oauthlib import OAuth1Session

base_authorization_url = "https://api.twitter.com/oauth/authorize"
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"


class TwitterAuth():
    def __init__(self, consumer_key: str, consumer_secret: str) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
        try:
            fetch_response = self.oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered."
            )
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)

        authorization_url = self.oauth.authorization_url(
            base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )

        oauth_tokens = oauth.fetch_access_token(access_token_url)

        self.access_token = oauth_tokens["oauth_token"]
        self.access_token_secret = oauth_tokens["oauth_token_secret"]

    def get_oauth(self):
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )
        return oauth
