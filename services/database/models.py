import logging
from mongoengine import Document, fields
from database.config import Mongo

logger = logging.getLogger(__name__)

mongo = Mongo()

try:
    mongo.connect()
except Exception as e:
    logger.warning(f"There is a problem in connecting to database. \n{e}")


class Auth(Document):
    key = fields.StringField()
    first_name = fields.StringField()
    last_name = fields.StringField()
    phone = fields.StringField()
