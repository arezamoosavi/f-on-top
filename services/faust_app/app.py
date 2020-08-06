import logging
import os
from datetime import datetime
from distutils.util import strtobool
from logging.config import dictConfig
from faust_app import producer
import faust

KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
STORE_URI = os.getenv("STORE_URI")

TOPIC_ALLOW_DECLARE = True
TOPIC_DISABLE_LEADER = False
TOPIC_NAME = os.getenv("KAFKA_TOPIC")

SSL_ENABLED = False
SSL_CONTEXT = None

LOGGING = dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "loggers": {"transactions": {"handlers": ["console"], "level": "DEBUG"}},
    }
)

DEBUG = strtobool(os.getenv("DEBUG", "no"))
app = faust.App(
    id="sample_app",
    debug=DEBUG,
    autodiscover=True,
    origin="faust_app",
    broker=KAFKA_BOOTSTRAP_SERVER,
    store=STORE_URI,
    logging_config=LOGGING,
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


async def is_exist_already(data: dict):
    pass


async def save_to_mongo(data: dict):
    pass


@app.agent(_topic)
async def raw_data_processor(stream):
    async for record in stream:
        check_result = await is_exist_already(record)
        logging.info(f"check data: \n{record}\n")
        if check_result:
            await save_to_mongo(record)
            logging.info(f"saved to mongo:\n{record}\n")

