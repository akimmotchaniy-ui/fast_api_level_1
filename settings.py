from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    URI: str
    DB_NAME: str = 'travel_agency'
    TOURS_COLLECTION: str = 'tours'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


settings = Settings()
