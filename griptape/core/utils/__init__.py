import json
from .j2 import J2
from .manifest_validator import ManifestValidator


def minify_json(value: str) -> str:
    return json.dumps(json.loads(value), separators=(',', ':'))


__all__ = [
    "J2",
    "ManifestValidator"
]
