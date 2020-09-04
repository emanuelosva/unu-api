"""
Unu API - Application settings.
"""

from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    General Application settings class.
    """

    class Config:
        """
        Get env variables from dotenv file.
        """
        env_file = ".env"

    ###########################################
    ##       General Configurations          ##
    ###########################################

    APP_NAME: str = "Unu - API"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGIN: List[str]
    EMAIL_ADMIN: str = "debuggers.master@gmail.com"
    API_URL: str

    ###########################################
    ##                Security               ##
    ###########################################

    SECRET_JWT: str = "secret"

    ###########################################
    ##               DataBase                ##
    ###########################################

    DB_NAME: str
    DB_PASSWORD: str
    DB_CLUSTER: str
    DB_USERNAME: str

    ###########################################
    ##         Email Configurations          ##
    ###########################################
    SENDGRID_API_KEY: str
    EMAIL_SENDER: str = "unu.events@gmail.com"

    ###########################################
    ##               Task Queue              ##
    ###########################################

    REDIS_URL: str
    QUEUES: List[str]

    ###########################################
    ##          External Storage             ##
    ###########################################

    GOOGLE_STORAGE_BUCKET: str
    ALLOWED_EXTENSIONS: List[str]
    GOOGLE_APPLICATION_CREDENTIALS: str


settings = Settings()
