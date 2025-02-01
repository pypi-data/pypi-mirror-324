import os

__all__ = ["config"]


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "MySecret")  # Change in production


config = Config()
