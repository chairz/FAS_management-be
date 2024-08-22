from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DEBUG
    DEBUG: bool
    PORT: int
    HOST: str

    # SQL
    SQL_HOST: str
    SQL_DATABASE: str
    SQL_USER: str
    SQL_PASSWORD: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = "config.env"  # path to .env file
        extra = "allow"


settings = Settings()  # Create an instance of Settings
