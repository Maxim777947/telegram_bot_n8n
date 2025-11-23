from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str | None = None
    DATABASE_URL: str | None = None

    TELEGRAM_TOKEN: str | None = None

    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None

    DB_TYPE: str | None = None
    DB_POSTGRESDB_HOST: str | None = None
    DB_POSTGRESDB_PORT: str | None = None

    DB_POSTGRESDB_USER: str | None = None
    DB_POSTGRESDB_PASSWORD: str | None = None
    DB_POSTGRESDB_DATABASE: str | None = None

    N8N_BASIC_AUTH_USER: str | None = None
    N8N_BASIC_AUTH_PASSWORD: str | None = None
    N8N_ENCRYPTION_KEY: str | None = None
    N8N_HOST: str | None = None
    N8N_EDITOR_BASE_URL: str | None = None
    WEBHOOK_URL: str | None = None
    BACKEND_URL: str | None = None
    API_BASE_URL: str | None = None

    # YandexGPT
    YANDEX_GPT_KEY: str | None = None
    YANDEX_GPT_CATALOG: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
