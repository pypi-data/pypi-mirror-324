import time
from pydantic import BaseModel
import json


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def get_schema_dict_from_pydanticmodel(model: BaseModel) -> dict:
    return model.model_dump()

def dict_to_json_file(data: dict, file_path: str):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
