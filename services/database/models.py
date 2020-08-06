import logging
from mongoengine import Document, fields
from database.config import Mongo

# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

mongo = Mongo()

try:
    mongo.connect()
except Exception as e:

    logging.warning(f"There is a problem in connecting to database. \n{e}")


class User(Document):
    _id = fields.StringField(primary_key=True)
    first_name = fields.StringField()
    last_name = fields.StringField()
    phone = fields.IntField()

    meta = {"db_alias": "defaultdb"}

