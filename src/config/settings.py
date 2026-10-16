from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str
    app_env: str = "development"
    debug: bool
    app_host: str
    app_port: int

    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: int
    postgres_db: str
    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    frontend_url: str
    jwt_secret_key: str
    refresh_token_days: int


settings = Settings()