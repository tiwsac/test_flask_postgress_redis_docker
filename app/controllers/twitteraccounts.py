from datetime import datetime

from model.twitteraccount_model import TwitterAccountModel
from common.base_sqlalchemy import delete_gracefully, commit_gracefully, add_refresh


def get_account(identifier, identifier_type):
    """
    Gets the account with the specified account id or screen name
    """
    if identifier_type == 'id':
        twitter_account_obj = TwitterAccountModel.query.filter_by(id=identifier).first()
    else:
        twitter_account_obj = TwitterAccountModel.query.filter_by(screen_name=identifier).first()

    if twitter_account_obj:
        response = {
            "Name": twitter_account_obj.name,
            "ScreenName": twitter_account_obj.screen_name,
            "FollowersCount":twitter_account_obj.followers_count,
            "FollowingCount": twitter_account_obj.following_count,
            "TweetsCount": twitter_account_obj.tweets_count,
            "ProfileImgUrl": twitter_account_obj.profile_image_url,
            "Description": twitter_account_obj.description,
            "Location": twitter_account_obj.location,
            "Protected": twitter_account_obj.protected,
            "Private": twitter_account_obj.private,
            "Url": twitter_account_obj.url
        }
    else:
        response = "No account found"

    return response


def create_account(data):
    """
    Creates an account from the given data
    """
    screen_name = data.get("ScreenName")
    if not screen_name:
        return "Screen Name is missing", 400

    twitter_account_obj = TwitterAccountModel.query.filter_by(screen_name=screen_name).first()

    if twitter_account_obj:
        return "Screen Name isn't available."

    new_twitter_account_obj = TwitterAccountModel(name=data.get("Name"),
                                                  screen_name=screen_name,
                                                  followers_count=data.get("FollowersCount"),
                                                  following_count=data.get("FollowingCount", 0),
                                                  tweets_count=data.get("TweetsCount", 0),
                                                  profile_image_url=data.get("ProfileImgUrl"),
                                                  description=data.get("Description"),
                                                  location=data.get("Location"),
                                                  protected=data.get("Protected", False),
                                                  private=data.get("Private", False),
                                                  url=data.get("Url"),
                                                  created_at=datetime.now())

    add_refresh(new_twitter_account_obj)
    response = {
        "Message": "Account created Successfully.",
        "AccountID": new_twitter_account_obj.id
    }

    return response


def update_account(data):
    """
    Updates a twitter account's details
    """
    screen_name =  data.get("ScreenName")
    if not screen_name:
        return "Screen Name is missing", 400

    twitter_account_obj = TwitterAccountModel.query.filter_by(screen_name=screen_name).first()
    if twitter_account_obj:
        if data.get("Name"):
            twitter_account_obj.name = data.get("Name")
        if data.get("FollowersCount"):
            twitter_account_obj.followers_count = data.get("FollowersCount")
        if data.get("FollowingCount"):
            twitter_account_obj.following_count = data.get("FollowingCount")
        if data.get("TweetsCount"):
            twitter_account_obj.tweets_count = data.get("TweetsCount")
        if data.get("ProfileImgUrl"):
            twitter_account_obj.profile_image_url = data.get("ProfileImgUrl")
        if data.get("Description"):
            twitter_account_obj.description = data.get("Description")
        if data.get("Location"):
            twitter_account_obj.location = data.get("Location")
        if data.get("Protected"):
            twitter_account_obj.protected = data.get("Protected")
        if data.get("Private"):
            twitter_account_obj.private = data.get("Private")
        if data.get("Url"):
            twitter_account_obj.url = data.get("Url")
        commit_gracefully()
        response = "Account updated Successfully."
    else:
        response = "No account found"

    return response


def delete_account(identifier, identifier_type):
    """
    Deletes an account from the database
    """
    if identifier_type == 'id':
        twitter_account_obj = TwitterAccountModel.query.filter_by(id=identifier).first()
    else:
        twitter_account_obj = TwitterAccountModel.query.filter_by(screen_name=identifier).first()

    if twitter_account_obj:
        delete_gracefully(twitter_account_obj)
        response = "Account deleted successfully"
    else:
        response = "No account found"

    return response
