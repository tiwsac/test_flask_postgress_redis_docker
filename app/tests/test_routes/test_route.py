from unittest import TestCase
import time
from main import app
from controllers import tweets as tweet_controllers
from unittest.mock import Mock
import psycopg2
from datetime import datetime

import configparser
import json

class TestRoutesTweet(TestCase):
    def test_get_tweet_response(self):
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


class TestTwitterAccount(TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()

    def test_get_twitter_account(self):
        """ Testing not available twitter account Read operation"""
        screen_name = "Test_get_" + str(time.time())
        result = self.app.get(f'/twitteraccount/{screen_name}?identifier_type=screen_name')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.get_data(as_text=True), "No account found")

    def test_delete_twitter_account(self):
        # Testing delete twitter account via screen_name
        screen_name = "Test_delete_" + str(time.time())
        result = self.app.delete(f'/twitteraccount/{screen_name}?identifier_type=screen_name')
        self.assertEqual(result.status_code, 200, "Delete account via id check")
        self.assertEqual(result.get_data(as_text=True), "No account found")

    def test_twitter_account(self):
        """ Testing CRUD operation of twitter account"""
        screen_name = "Test_" + str(time.time())
        twitter_acccount_details = {
            "Name": "Test account",
            "ScreenName": screen_name,
            "FollowersCount": 300,
            "FollowingCount": 100,
            "TweetsCount": 500,
            "ProfileImgUrl": "https://pbs.twimg.com/profile_images/1328081183108964353/zbGwjfmw_normal.jpg",
            "Description": "hello world",
            "Location": "Test",
            "Protected": False,
            "Private": False,
            "Url": "https://t.co/8iKgX9VpFy"
        }

        # ----------------------------------- Create Operation -----------------------------------
        # Testing new twitter account creation.
        result = self.app.post('/twitteraccount', json=twitter_acccount_details)
        response = json.loads(result.get_data(as_text=True))
        twitter_acc_id = response["AccountID"]
        self.assertEqual(result.status_code, 200, "Account created Successfully.")
        self.assertEqual(response["Message"], "Account created Successfully.")

        # Testing new twitter account creation with the already existing screen_name.
        result = self.app.post('/twitteraccount', json=twitter_acccount_details)
        self.assertEqual(result.status_code, 200, "Screen Name isn't available.")
        self.assertEqual(result.get_data(as_text=True), "Screen Name isn't available.")

        # Testing new twitter account creation where screen_name missing.
        del twitter_acccount_details["ScreenName"]
        result = self.app.post('/twitteraccount', json=twitter_acccount_details)
        self.assertEqual(result.status_code, 400, "Screen Name is missing")
        self.assertEqual(result.get_data(as_text=True), "Screen Name is missing")
        twitter_acccount_details["ScreenName"] = screen_name

        # ----------------------------------- Read Operation -----------------------------------
        # Testing get twitter account via screen_name.
        result = self.app.get(f'/twitteraccount/{screen_name}?identifier_type=screen_name')
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get account via screen_name status check")
        self.assertEqual(response, twitter_acccount_details)

        # Testing get twitter account via id.
        result = self.app.get(f'/twitteraccount/{twitter_acc_id}?identifier_type=id')
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get account via ID status check")
        self.assertEqual(response, twitter_acccount_details)

        # ----------------------------------- Update Operation -----------------------------------
        # Testing update twitter account.
        twitter_acccount_details["Description"] = "Update in description"
        twitter_acccount_details["Location"] = "New Location"
        twitter_acccount_details["Private"] = True
        result = self.app.put(f'/twitteraccount', json=twitter_acccount_details)
        self.assertEqual(result.status_code, 200, "update account check")
        self.assertEqual(result.get_data(as_text=True), "Account updated Successfully.")

        # Testing update twitter account screen_name missing.
        del twitter_acccount_details["ScreenName"]
        result = self.app.put(f'/twitteraccount', json=twitter_acccount_details)
        self.assertEqual(result.status_code, 400, "update account screen name missing check ")
        self.assertEqual(result.get_data(as_text=True), "Screen Name is missing")
        twitter_acccount_details["ScreenName"] = screen_name

        # Testing update twitter account not found.
        twitter_acccount_details["ScreenName"] = screen_name + "missing_account"
        result = self.app.put(f'/twitteraccount', json=twitter_acccount_details)
        self.assertEqual(result.status_code, 200, "update account account not found check")
        self.assertEqual(result.get_data(as_text=True), "No account found")

        # ----------------------------------- Read Operation -----------------------------------
        # Testing get twitter account via screen_name after updating the twitter account.
        twitter_acccount_details["ScreenName"] = screen_name
        result = self.app.get(f'/twitteraccount/{screen_name}?identifier_type=screen_name')
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get account via screen_name status after update check")
        self.assertEqual(response, twitter_acccount_details)

        # ----------------------------------- Delete Operation -----------------------------------
        # Testing delete twitter account via id
        result = self.app.delete(f'/twitteraccount/{twitter_acc_id}?identifier_type=id')
        self.assertEqual(result.status_code, 200, "Delete account via id check")
        self.assertEqual(result.get_data(as_text=True), "Account deleted successfully")


class TestTweet(TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()
        # Creating test twitter account
        twitter_account_screen_name = "Test_tweet_" + str(time.time())
        twitter_acccount_details = {
            "Name": "Test account",
            "ScreenName": twitter_account_screen_name,
            "FollowersCount": 300,
            "FollowingCount": 100,
            "TweetsCount": 500,
            "ProfileImgUrl": "https://pbs.twimg.com/profile_images/1328081183108964353/zbGwjfmw_normal.jpg",
            "Description": "hello world",
            "Location": "Test",
            "Protected": False,
            "Private": False,
            "Url": "https://t.co/8iKgX9VpFy"
        }
        result = self.app.post('/twitteraccount', json=twitter_acccount_details)
        response = json.loads(result.get_data(as_text=True))
        twitter_acc_id = response["AccountID"]
        sqls = []
        tweet_text = "Test_borg"
        arr = '{}'
        for i in range(11):
            sql = f"INSERT INTO tweet(text, urls, hashtags, symbols, user_mentions, in_reply_to_status_id, in_reply_to_user_id," \
                  f" quoted_status_id, quoted_user_id, retweeted_status_id, retweeted_user_id, is_status, author_id, retweet_count," \
                  f" created_at, favorite_count) VALUES ('{tweet_text + str(i)}', '{arr}', '{arr}', '{arr}', '{arr}', 0, 0, 0, 0, 0, 0, {False}," \
                  f"{twitter_acc_id}, 0, '{datetime.now()}', {99999991 - i})"
            sqls.append(sql)

        conn = psycopg2.connect(database="app", user='postgres', password='postgres', host='borg_test_host', port= '5432')
        cur = conn.cursor()
        for sql in sqls:
            cur.execute(sql)

        conn.commit()

        ids = []
        for i in range(11):
            cur.execute(f"SELECT id FROM tweet WHERE author_id = {twitter_acc_id} AND text = '{tweet_text + str(i)}'")
            tweet_id = cur.fetchone()
            ids.append(tweet_id[0])

        self.tweet_ids = ids
        self.twitter_acc_id = twitter_acc_id
        self.tweet_text_prefix = tweet_text
        self.twitter_account_screen_name = twitter_account_screen_name
        cur.close()
        conn.close()

    def tearDown(self) -> None:
        conn = psycopg2.connect(database="app", user='postgres', password='postgres', host='borg_test_host', port='5432')
        cur = conn.cursor()

        # Deleting test tweets
        for id in self.tweet_ids:
            sql = f'''DELETE FROM tweet WHERE id = {id}'''
            cur.execute(sql)

        # Deleting test tweet account
        sql = f'''DELETE FROM twitteraccount WHERE id = {self.twitter_acc_id}'''
        cur.execute(sql)

        conn.commit()
        cur.close()
        conn.close()

    def test_get_tweet(self):
        """ Testing get tweet"""
        tweet_id = 99999999
        result = self.app.get(f'/tweets/{tweet_id}')
        self.assertEqual(result.status_code, 200, "Get tweet not found check")
        self.assertEqual(result.get_data(as_text=True), "Tweet Not found")

        # Testing for valid tweet get call
        result = self.app.get(f'/tweets/{self.tweet_ids[0]}')
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get tweet check")
        self.assertEqual(response["TweetTxt"], self.tweet_text_prefix + str(0), "Tweet found text check")

    def test_top_tweet(self):
        """ Testing top tweet"""
        result = self.app.get(f'/tweets/top')
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get top tweet check")
        self.assertEqual(len(response["Tweets"]), 10, "Getting 10 tweets")
        i = 0
        for tweet in response["Tweets"]:
            self.assertEqual(tweet["TweetTxt"], self.tweet_text_prefix + str(i), f"Top {i+1} tweet text check")
            i += 1

    def test_account_top_tweet(self):
        """ Testing total top tweets """
        # Testing top tweets via twitter account id
        result = self.app.get(f"/tweets/account/top/{self.twitter_acc_id}?identifier_type=id")
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get top account tweet via id check")
        self.assertEqual(len(response["Tweets"]), 10, "Getting total account top tweets check")
        i = 0
        for tweet in response["Tweets"]:
            self.assertEqual(tweet["TweetTxt"], self.tweet_text_prefix + str(i), f"Top {i+1} tweet text via id check")
            i += 1

        # Testing top tweets via twitter account screen_name
        result = self.app.get(f"/tweets/account/top/{self.twitter_account_screen_name}?identifier_type=screen_name")
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get top account tweet via screen_name check")
        self.assertEqual(len(response["Tweets"]), 10, "Getting top account top tweets check")
        i = 0
        for tweet in response["Tweets"]:
            self.assertEqual(tweet["TweetTxt"], self.tweet_text_prefix + str(i), f"Top {i + 1} tweet text via screen_name check")
            i += 1

    def test_account_all_tweet(self):
        """ Testing all tweets """
        # Testing all tweets via twitter account id
        result = self.app.get(f"/tweets/account/{self.twitter_acc_id}?identifier_type=id")
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get account tweet via id check")
        self.assertEqual(response["PageSize"], 20, "Getting pagesize check")
        self.assertEqual(response["TotalTweetCount"], 11, "Getting all account tweets check")
        i = 10
        for tweet in response["Tweets"]:
            self.assertEqual(tweet["TweetTxt"], self.tweet_text_prefix + str(i), f"Top {i+1} tweet text check")
            i -= 1

        # Testing all tweets via twitter account screen_name
        result = self.app.get(f"/tweets/account/{self.twitter_account_screen_name}?identifier_type=screen_name")
        response = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 200, "Get account tweet via screen_name check")
        self.assertEqual(response["PageSize"], 20, "Getting pagesize check")
        self.assertEqual(response["TotalTweetCount"], 11, "Getting all account tweets check")
        i = 10
        for tweet in response["Tweets"]:
            self.assertEqual(tweet["TweetTxt"], self.tweet_text_prefix + str(i), f"Top {i + 1} tweet text check")
            i -= 1