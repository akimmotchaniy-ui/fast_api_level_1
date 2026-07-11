from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    URI: str
    SHOP_NAME_DB: str = 'shop_project'
    BOOKS_COLLECTION: str = 'books'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


settings = Settings()
