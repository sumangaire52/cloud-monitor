from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AZURE_SUBSCRIPTION_ID: str = "abcd"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env = Settings()
