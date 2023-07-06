from common.base_sqlalchemy import db
from sqlalchemy import Text, BIGINT, Integer, Column, BOOLEAN, DateTime, text


class TwitterAccountModel(db.Model):
    __tablename__ = "twitteraccount"


    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    screen_name = Column(Text, nullable=False, unique=True) # Making screen Name Unique
    followers_count = Column(Integer, server_default=text("0"), nullable=False)
    following_count = Column(Integer, server_default=text("0"), nullable=False)
    tweets_count = Column(Integer, server_default=text("0"), nullable=False)
    profile_image_url = Column(Text)
    description = Column(Text)
    location = Column(Text)
    protected = Column(BOOLEAN, server_default=text("FALSE"), nullable=False)
    private = Column(BOOLEAN, server_default=text("FALSE"), nullable=False)
    url = Column(Text)
    created_at = Column(DateTime, server_default=text("NOW()"), nullable=False)
