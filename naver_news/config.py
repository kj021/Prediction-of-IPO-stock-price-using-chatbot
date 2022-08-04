import json
from pathlib import Path
from typing import Optional


def get_secret(
    key: str,
    default_value: Optional[str] = None,
    json_path= "C:/Users/KHS/Desktop/카카오톡 봇/Prediction-of-IPO-stock-price-using-chatbot/secret.json"
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")


client_id = get_secret("client_id")
client_secret = get_secret("client_secret")