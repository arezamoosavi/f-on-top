import logging
import os
import faust

from datetime import datetime
from distutils.util import strtobool
from logging.config import dictConfig
from database.models import Auth


KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
STORE_URI = os.getenv("STORE_URI")
TOPIC_NAME = os.getenv("KAFKA_TOPIC")


# loging
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

app = faust.App(
    id="sample_app",
    autodiscover=True,
    origin="faust_app",
    broker=KAFKA_BOOTSTRAP_SERVER,
    store=STORE_URI,
)


agent_topic = app.topic(TOPIC_NAME, acks=False, partitions=None)


async def save_to_mongo(data):
    u = Auth(
        key=str(data["key"]),
        first_name=str(data["first_name"]),
        last_name=str(data["last_name"]),
        phone=str(data["phone"]),
    )
    u.save()
    logging.info(f"saved to mongo:\n{data}\n")


@app.agent(agent_topic)
async def auth_data_processor(stream):
    async for record in stream:
        if "key" in record.keys() and record["key"]:
            u = Auth.objects(key=str(record["key"])).first()
            if u:
                logging.info(f"{u} is used already!")
            else:
                await save_to_mongo(record)
        else:
            logging.info(f"key field is necessary")
        yield " yeah :> "

