from common.base_sqlalchemy import db
from sqlalchemy import Text, ARRAY, BIGINT, Integer, Column, BOOLEAN, DateTime, text as alchText, ForeignKey


class TweetModel(db.Model):
    __tablename__ = "tweet"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    urls = Column(ARRAY(Text))
    hashtags = Column(ARRAY(Text))
    symbols = Column(ARRAY(Text))
    user_mentions = Column(ARRAY(Text))
    in_reply_to_status_id = Column(BIGINT)
    in_reply_to_user_id = Column(BIGINT)
    quoted_status_id = Column(BIGINT)
    quoted_user_id = Column(BIGINT)
    retweeted_status_id = Column(BIGINT)
    retweeted_user_id = Column(BIGINT)
    is_status= Column(BOOLEAN)
    author_id = Column(BIGINT, ForeignKey("customer.id"), nullable=False)
    retweet_count = Column(Integer, server_default=alchText("0"))
    created_at = Column(DateTime(), server_default=alchText("NOW()"), nullable=False)
    favorite_count = Column(Integer, server_default=alchText("0"))
