import pathlib
from functools import cache

from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploaded"
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_auth_token: str
    debug: bool = False
    echo_active: bool = False
    app_auth_token_prod: str = None
    skip_auth: bool = False

    class Config:
        env_file = str(BASE_DIR.parent.parent / ".env")
