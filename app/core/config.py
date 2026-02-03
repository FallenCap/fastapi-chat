from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str | None = None
    MONGO_URI: str | None = None
    DB_NAME: str | None = None
    JWT_SECRET: str | None = None
    JWT_ALGORITHM: str | None = None
    JWT_EXPIRE: int | None = None
    KAFKA_BROKER_URL: str | None = None
    KAFKA_TOPIC: str | None = None
    KAFKA_CONSUMER_ID: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
