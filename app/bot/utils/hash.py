import hashlib
import hmac
from app.config import settings


def hash_value(value):
    return hmac.new(
        bytes(settings.SECRET_KEY, "utf-8"), value.encode(), hashlib.sha256
    ).hexdigest()
