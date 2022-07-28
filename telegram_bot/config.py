import json
from pathlib import Path
from typing import Optional


def get_secret(
    key: str,
    default_value: Optional[str] = None,
    json_path= "C:/Users/KHS/Desktop/대학교/데이터 청년 캠퍼스/깃허브/Prediction-of-IPO-stock-price-using-chatbot/secret.json"
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} environment variable.")


api_key = get_secret("api_key")
chat_id = get_secret("chat_id")

