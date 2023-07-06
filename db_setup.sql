begin;

CREATE TABLE IF NOT EXISTS twitteraccount (
    id bigserial PRIMARY KEY,
    name text,
    screen_name text,
    followers_count int,
    following_count int,
    tweets_count int,
    profile_image_url text NULL,
    description text NULL,
    location text NULL,
    created_at timestamp,
    protected boolean,
    private boolean
);

CREATE TABLE IF NOT EXISTS tweet (
    id bigserial PRIMARY KEY,
    text text,
    urls text [],
    hashtags text [],
    symbols text [],
    user_mentions text [],
    in_reply_to_status_id bigint NULL,
    in_reply_to_user_id bigint NULL,
    quoted_status_id bigint NULL,
    quoted_user_id bigint NULL,
    retweeted_status_id bigint NULL,
    retweeted_user_id bigint NULL,
    is_status boolean,
    author_id bigint,
    retweet_count int,
    favorite_count int,
    created_at timestamp
);

end;