from flask_sqlalchemy import SQLAlchemy
from flask_restx import abort

from app import app

# Below values can be put in config file and better if we put it in Secret Manager. Different config values can be
# used for different ENV (dev/Production/QA). I am putting it here for simplicity.
# possgress_user = "postgres"
# possgress_password = "postgres"
# possgress_host = "borg_test_host"
# possgress_port = 5432
# possgress_db = "app"
#
# app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{possgress_user}:{possgress_password}@{possgress_host}:{possgress_port}/{possgress_db}"

db = SQLAlchemy(app)

sql_session = db.session


def add_refresh(entity: db.Model):
    """Adds the `entity` to db and fetches back the entity (where some values can be
    extra due to auto-increment & default values)"""
    sql_session.add(entity)
    commit_gracefully()
    sql_session.refresh(entity)


def delete_gracefully(entity: db.Model):
    """ Tries to delete the given entity """
    try:
        sql_session.delete(entity)
        sql_session.commit()
    except:
        abort(400, "Issue with DB Delete")


def commit_gracefully():
    """Tries to commit the db operation"""
    try:
        sql_session.commit()
    except:
        abort(400, "Issue with DB commit")



