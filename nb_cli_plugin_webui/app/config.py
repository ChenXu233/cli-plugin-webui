import os
import json
from enum import Enum
from typing import Any
from pathlib import Path

from pydantic import Field, BaseModel, SecretStr

from .utils.security import salt
from .utils.storage import get_config_file

CONFIG_FILE = "config.json"
CONFIG_FILE_PATH = get_config_file(CONFIG_FILE)


class LogLevels(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class SpecialTypeJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, SecretStr):
            return o.get_secret_value()
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


class AppConfig(BaseModel):
    base_dir: str = Field(
        default_factory=lambda: (
            str(Path.cwd() / "/projects") if "WEBUI_BUILD" in os.environ else str()
        ),
        description="基础目录，创建实例将由此开始",
    )
    host: str = Field(default="localhost", description="主机名")
    port: str = Field(default="12345", description="端口号")
    debug: int = Field(default=0, description="是否开启调试模式")
    enable_api_document: bool = Field(default=False, description="是否开启 API 文档")

    log_level: LogLevels = Field(default=LogLevels.INFO, description="日志等级")
    log_is_store: bool = Field(default=False, description="是否存储日志")

    secret_key: SecretStr = Field(default=SecretStr(str()), description="验证密钥的密钥")
    hashed_token: SecretStr = Field(default=SecretStr(str()), description="哈希后的 token")
    salt: SecretStr = Field(default=SecretStr(str()), description="盐值")

    allowed_origins: list = Field(
        default=["*"],
        description="限定访问来源",
    )

    process_log_destroy_seconds: int = Field(
        default=5 * 60, description="进程单条日志销毁时间（秒）"
    )

    extension_store_visible_items: int = Field(default=12, description="扩展商店每页显示数量")

    @property
    def log_level_str(self) -> str:
        return self.log_level.value

    def to_json(self) -> str:
        return json.dumps(
            self.model_dump(mode="python"),
            cls=SpecialTypeJSONEncoder,
            indent=2,
            ensure_ascii=False,
        )

    def reset_token(self, token: str) -> None:
        self.salt = SecretStr(salt.gen_salt())
        self.hashed_token = SecretStr(
            salt.get_token_hash(self.salt.get_secret_value() + token)
        )

    def check_necessary_config(self) -> bool:
        return bool(
            self.base_dir and self.secret_key and self.hashed_token and self.salt
        )

    def get_description(self, field_name: str) -> str | None:
        return self.__class__.model_fields[field_name].description

class ConfigParser(AppConfig):
    def load(self, path: Path):
        new_conf = AppConfig.model_validate_json(path.read_text(encoding="utf-8"))
        for name in self.model_fields:
            setattr(self, name, getattr(new_conf, name))

    def store(self, path: Path):
        path.write_text(self.to_json(), encoding="utf-8")


Config = ConfigParser()
