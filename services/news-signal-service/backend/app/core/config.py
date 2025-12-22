import secrets
import warnings
from pathlib import Path
from typing import Any, List, Optional, Literal

from pydantic import AnyUrl, EmailStr, BaseSettings, validator
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def parse_cors(v: Any) -> List[str]:
    if isinstance(v, str):
        return [i.strip() for i in v.split(",") if i.strip()]
    if isinstance(v, list):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    PROJECT_NAME: str = "news-signal-service"

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    SENTRY_DSN: Optional[AnyUrl] = None

    BACKEND_CORS_ORIGINS: str = "" #List[str] = []

    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_DB: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    KAFKA_KEYWORD_TOPIC: str
    KAFKA_BOOTSTRAP_SERVERS: List[str] = ["localhost:9092"]

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        env_file = "../.env"
        case_sensitive = True

    # ---------- validators ----------

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors(cls, v):
    #     return parse_cors(v)

    @validator("EMAILS_FROM_NAME", always=True)
    def set_default_email_name(cls, v, values):
        return v or values.get("PROJECT_NAME")

    @validator("SECRET_KEY", "MYSQL_PASSWORD", "FIRST_SUPERUSER_PASSWORD")
    def check_default_secrets(cls, v, field, values):
        if v == "changethis":
            msg = f'The value of {field.name} is "changethis". Please change it.'
            if values.get("ENVIRONMENT") == "local":
                warnings.warn(msg)
            else:
                raise ValueError(msg)
        return v

    # ---------- computed properties ----------

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return URL.create(
            drivername="mysql+mysqlconnector",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            database=self.MYSQL_DB,
        ).render_as_string(hide_password=False)

    # @property
    # def all_cors_origins(self) -> List[str]:
    #     return [o.rstrip("/") for o in self.BACKEND_CORS_ORIGINS] + [
    #         self.FRONTEND_HOST.rstrip("/")
    #     ]

    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)


settings = Settings()
