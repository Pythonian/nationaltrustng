import tweepy
from django.conf import settings


def post_tweet(blog_post):
    # Authenticate with Twitter using your API credentials
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Compose the tweet message
    tweet = f"New blog post: '{blog_post.title}' - {blog_post.get_absolute_url()}"
    print(tweet)

    # Post the tweet
    api.update_status(tweet)
