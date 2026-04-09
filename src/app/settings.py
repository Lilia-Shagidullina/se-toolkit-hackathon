from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    name: str = "Joke Bot Web"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "jokebot"
    db_user: str = "postgres"
    db_password: str = "postgres"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
