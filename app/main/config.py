import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv('TOKEN')
    CARD_RARES = os.getenv('RARES')

config = Config
