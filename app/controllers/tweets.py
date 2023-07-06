import json

from model.tweet_model import TweetModel
from model.twitteraccount_model import TwitterAccountModel
from app import cache

def get_tweet_response(tweet_obj:TweetModel):
    if tweet_obj:
        response= {
            "TweetTxt": tweet_obj.text,
            "Urls": tweet_obj.urls,
            "Hashtags": tweet_obj.hashtags,
            "Symbols": tweet_obj.symbols,
            "UserMentions": tweet_obj.user_mentions,
            "RetweetCount": tweet_obj.retweet_count,
            "FavoriteCount": tweet_obj.favorite_count

        }
    else:
        response = "Tweet Not found"

    return response


def get_tweet(id):
    """
    Gets the tweet details with the given id
    """
    tweet_obj = TweetModel.query.filter_by(id=id).first()
    return get_tweet_response(tweet_obj)


def get_account_tweets(identifier, identifier_type):
    """
    Gets the tweets for a given account max 20 tweets
    """
    if identifier_type == 'id':
        twitter_account_obj = TwitterAccountModel.query.filter_by(id=identifier).first()
    else:
        twitter_account_obj = TwitterAccountModel.query.filter_by(screen_name=identifier).first()

    # We have to add pagination to make the API response limited to improve the performance and add the pagination
    # in the API. I am not adding pagination here. I am using static values of pagination here.
    # Here I am shorting tweets on the bases of descending order their created_at time.
    page_no = 1
    page_size = 20
    query = TweetModel.query.filter_by(author_id=twitter_account_obj.id).order_by(
        TweetModel.created_at.desc())

    tweet_count = query.count()
    tweet_objs = query.limit(page_size).offset((page_no - 1) * page_size).all()

    response = {
        "Tweets": [get_tweet_response(tweet_obj) for tweet_obj in tweet_objs],
        "TotalTweetCount": tweet_count,
        "Page": page_no,
        "PageSize": page_size
    }
    return response


def get_top_tweets():
    """
    Gets the top 10 tweets by favourite count
    """
    top_tweet_cache_key = "top_tweets"
    if cache.get(top_tweet_cache_key):
        response = json.loads(cache.get(top_tweet_cache_key))
    else:
        tweet_objs = TweetModel.query.order_by(TweetModel.favorite_count.desc()).limit(10).all()
        # I am not adding Author information for the tweet as I am not seeing that requirement.
        response = {
            "Tweets": [get_tweet_response(tweet_obj) for tweet_obj in tweet_objs]
        }
        top_tweet_cache_vlaue = json.dumps(response)
        cache.set(top_tweet_cache_key, top_tweet_cache_vlaue)
    return response


def get_account_top_tweets(identifier, identifier_type):
    """
    Gets the top 10 tweets by favourite count for a given twitter account
    """
    if identifier_type == 'id':
        twitter_account_obj = TwitterAccountModel.query.filter_by(id=identifier).first()
    else:
        twitter_account_obj = TwitterAccountModel.query.filter_by(screen_name=identifier).first()

    tweet_objs = []
    if twitter_account_obj:
        tweet_objs = TweetModel.query.filter_by(author_id=twitter_account_obj.id).order_by(
            TweetModel.favorite_count.desc()).limit(10).all()

    response = {
        "Tweets": [get_tweet_response(tweet_obj) for tweet_obj in tweet_objs]
    }

    response["TweetAuthor"] = twitter_account_obj.name

    return response