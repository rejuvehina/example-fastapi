from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithmn: str
    access_token_expire_minutes: int
# now we have to tell pydantic import it from .env file
    class Config:
        env_file = ".env"

settings = Settings()