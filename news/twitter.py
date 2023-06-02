import tweepy
from django.conf import settings

def post_tweet(blog_post):
    # Twitter API credentials
    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Compose the tweet message
    tweet = f"New blog post: '{blog_post.title}' - {blog_post.get_absolute_url()}"

    # Post the tweet
    api.update_status(tweet)

