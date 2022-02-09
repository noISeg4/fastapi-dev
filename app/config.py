from pydantic import BaseSettings

#  searches for the following keys in the environment variables
#  variable values overridden by environment variables

#  can also provide default values
#  database_hostname: str = "localhost"
#  database_username: str = "postgres"
class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # import values from .env file
    class Config:
        env_file = ".env"

settings = Settings()