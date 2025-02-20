import hmac
import json
from hashlib import sha256
from urllib.parse import parse_qsl

from starlette.requests import Request

from app.config import settings


def tg_auth(request: Request):
    if not settings.AUTH:
        return 1
    if not "authorization" in request.headers or not request.headers.get(
        "authorization"
    ):
        raise ValueError
    data = parse_init_data(settings.BOT_TOKEN, request.headers.get("authorization"))
    user_id = data["user"]["id"]
    return user_id


def parse_init_data(token: str, raw_init_data: str):
    is_valid = validate_init_data(token, raw_init_data)
    if not is_valid:
        raise ValueError

    result = {}
    for key, value in parse_qsl(raw_init_data):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            result[key] = value
        else:
            result[key] = value
    print(result)
    return result


def validate_init_data(token, raw_init_data):
    try:
        parsed_data = dict(parse_qsl(raw_init_data))
    except ValueError:
        return False
    if "hash" not in parsed_data:
        return False

    init_data_hash = parsed_data.pop("hash")
    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(parsed_data.items())
    )
    secret_key = hmac.new(key=b"WebAppData", msg=token.encode(), digestmod=sha256)

    return (
        hmac.new(secret_key.digest(), data_check_string.encode(), sha256).hexdigest()
        == init_data_hash
    )
