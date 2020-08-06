import asyncio
import pytest
import json

from datetime import datetime
from faust_app.app import auth_data_processor, save_to_mongo
from database.models import Auth


# Opening JSON file
with open("tests/datasets/true_data.json") as json_file:
    true_data = json.load(json_file)


@pytest.mark.asyncio
async def test_auth_data_processor(mock_mongo, mock_faust):
    async with auth_data_processor.test_context() as agent:
        await agent.ask(value=true_data["v1"])

    p = Auth.objects(key=true_data["v1"]["key"])
    p_obj = p.first()
    counteer = p.count()
    assert counteer == 1
    assert p_obj.first_name == true_data["v1"]["first_name"]
    assert p_obj.phone == true_data["v1"]["phone"]


@pytest.mark.asyncio
async def test_fnc_save_to_mongo(mock_mongo):
    await save_to_mongo(true_data["v2"])

    p = Auth.objects(key=true_data["v2"]["key"])
    p_obj = p.first()
    counteer = p.count()
    assert counteer == 1
    assert p_obj.first_name == true_data["v2"]["first_name"]
    assert p_obj.phone == true_data["v2"]["phone"]
