import os

__all__ = ["config"]


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "MySecret") 
    API_KEY = os.getenv("API_KEY", "defaultkey") 


config = Config()
