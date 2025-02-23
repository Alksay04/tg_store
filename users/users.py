import json
import os

user_configs = os.path.join(os.path.dirname(__file__), 'configs')

def write_user_config(user_id: str, config: dict):
    with open(os.path.join(user_configs, f'{user_id}.json'), 'w+') as f:
        json.dump(config, f)


def read_user_config(user_id: str):
    with open(os.path.join(user_configs, f'{user_id}.json'), 'r') as f:
        return json.load(f)