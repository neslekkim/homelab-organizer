from pathlib import Path

import environ

from .django_common import MEDIA_ROOT

env = environ.FileAwareEnv()
env.prefix = "HLO_"

INPUT_FOLDER: Path = Path(
    env("INPUT_FOLDER", default="./input"),
).resolve()

JSON_SCHEMA: Path = Path(
    env("JSON_SCHEMA", default="./schema/webshop-orders.json"),
).resolve()

# Instance of https://github.com/dersimn/brother_ql_web or a fork
# with a simmilar api endpoint for printing images
BQW_ENDPOINT: str = env("BQW_ENDPOINT", default=None)

BARCODE_CACHE: Path = (MEDIA_ROOT / Path("barcode_cache")).resolve()
if not BARCODE_CACHE.is_dir():
    BARCODE_CACHE.mkdir(exist_ok=True)

QR_URL_PREFIX: str = env("QR_URL_PREFIX", default="")

OPENAPI_PROJECT_API_KEY: str = env("OPENAPI_PROJECT_API_KEY", default="")
OPENAPI_TITLE_CLEANUP_QUERY: str = env(
    "OPENAPI_TITLE_CLEANUP_QUERY",
    default=(
        "Can you make the title '{title}' shorter and more spesific? "
        "If possible, mention it's size or dimentions, but do not "
        "mention quantity, what it is used for, or how it is used."
    ),
)

OPENAPI_TITLE_CLEANUP_MODEL: str = env(
    "OPENAPI_TITLE_CLEANUP_MODEL",
    default="gpt-4",
)
