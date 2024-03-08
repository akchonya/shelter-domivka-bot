from pydantic import SecretStr, BaseModel
from pydantic_settings import BaseSettings as _BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlalchemy import URL


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


class BotConfig(BaseSettings, env_prefix="BOT_"):
    """
    Bot related settings
    """

    token: SecretStr
    drop_pending_updates: bool
    admin_chat_id: int


class DbCongig(BaseSettings, env_prefix="DB_"):
    """
    Database related settings with build_url() method
    """

    host: str
    db: str
    password: SecretStr
    port: int
    user: str
    data: str

    def build_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )


class AppConfig(BaseModel):
    bot: BotConfig
    db: DbCongig


def create_config() -> AppConfig:
    return AppConfig(bot=BotConfig(), db=DbCongig())