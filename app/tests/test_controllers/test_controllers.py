from unittest import TestCase
from controllers import tweets as tweet_controllers
from unittest.mock import Mock

class TestRoutesTweet(TestCase):
    def test_get_tweet_response(self):
        """ Testing get_tweet_response function """
        tweet_obj = None
        actual_response = tweet_controllers.get_tweet_response(tweet_obj)
        expected_response = "Tweet Not found"
        self.assertEqual(actual_response, expected_response)

        tweet_obj = Mock(text="Test Tweet", urls=["https://youtu.be/h-BY4DntQi8"], hashtags=["#test", "#hello_world"], symbols=[], user_mentions=[], retweet_count=20, favorite_count=50)
        expected_response = {"TweetTxt":"Test Tweet",
                             "Urls":["https://youtu.be/h-BY4DntQi8"],
                             "Hashtags":["#test", "#hello_world"],
                             "Symbols":[], "UserMentions":[],
                             "RetweetCount":20,
                             "FavoriteCount":50}
        actual_response = tweet_controllers.get_tweet_response(tweet_obj)
        self.assertEqual(actual_response, expected_response)