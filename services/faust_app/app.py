import logging
import os
import faust

from datetime import datetime
from distutils.util import strtobool
from database.models import Auth


KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
STORE_URI = os.getenv("STORE_URI")

TOPIC_ALLOW_DECLARE = True
TOPIC_DISABLE_LEADER = False
TOPIC_NAME = os.getenv("KAFKA_TOPIC")

SSL_ENABLED = False
SSL_CONTEXT = None
DEBUG = strtobool(os.getenv("DEBUG", "no"))

app = faust.App(
    id="sample_app",
    debug=DEBUG,
    autodiscover=True,
    origin="faust_app",
    broker=KAFKA_BOOTSTRAP_SERVER,
    store=STORE_URI,
    topic_allow_declare=TOPIC_ALLOW_DECLARE,
    topic_disable_leader=TOPIC_DISABLE_LEADER,
    broker_credentials=SSL_CONTEXT,
)

_topic = app.topic(TOPIC_NAME, acks=False, partitions=None)

# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

auth_field = ["key", "first_name", "last_name", "phone"]


async def save_to_mongo(data: dict):

    if auth_field == data.keys():
        u = Auth(
            key=data["key"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
        )
        u.save()
        logging.info(f"saved to mongo:\n{data}\n")
    else:
        logging.info(f"Some issue with data fields \n{data}\n")


@app.agent(_topic)
async def raw_data_processor(stream):
    async for record in stream:
        if "key" in record.keys() and record["key"]:
            u = Auth.objects(key=str(record["key"]))
            if u:
                logging.info(f"{u} is used already!")
            else:
                await save_to_mongo(record)
        else:
            logging.info(f"key field is necessary")

