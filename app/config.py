"""
Unu API - Application settings.
"""

import os

from typing import List
from pydantic import BaseSettings

from dotenv import load_dotenv

# Get env variables from dotenv files for development
load_dotenv()


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
    CORS_ORIGIN: List[str] = ["*"]
    EMAIL_ADMIN: str = "debuggers.master@gmail.com"
    API_URL: str = os.getenv("API_URL")

    ###########################################
    ##                Security               ##
    ###########################################

    SECRET_JWT: str = os.getenv("SECRET_JWT")

    ###########################################
    ##               DataBase                ##
    ###########################################

    DB_NAME: str = os.getenv("DB_NAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_CLUSTER: str = os.getenv("DB_CLUSTER")
    DB_USERNAME: str = os.getenv("DB_USERNAME")

    ###########################################
    ##         Email Configurations          ##
    ###########################################
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY")
    EMAIL_SENDER: str = "unu.events@gmail.com"

    ###########################################
    ##               Task Queue              ##
    ###########################################

    REDIS_URL: str = os.getenv("REDIS_URL")
    QUEUES: List[str] = ["email", "default"]

    ###########################################
    ##          External Storage             ##
    ###########################################

    GOOGLE_STORAGE_BUCKET: str = os.getenv("GOOGLE_STORAGE_BUCKET")
    ALLOWED_EXTENSIONS: List[str] = ["png", "jpg", "jpeg"]
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


settings = Settings()
