from _typeshed import Incomplete
from pydantic_settings import BaseSettings

class ClickPyDataBaseSetting(BaseSettings):
    model_config: Incomplete
    HOST: str
    SECURE: bool
    USERNAME: str
    PASSWORD: str

CLICK_PY_DATA_BASE_SETTING: Incomplete
