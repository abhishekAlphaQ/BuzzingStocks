import os
from pydantic import  BaseSettings

class DynamoDBSettings(BaseSettings):
    BUZZ_TABLE = os.getenv('BUZZ_TABLE')