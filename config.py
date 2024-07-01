import os

class Config:
    API_ID = ""
    API_HASH = ""
    BOT_TOKEN = ""
    BOT_SESSION = "" 
    DATABASE_URI = ""
    DATABASE_NAME = ""
    OWNER_ID = [int(id) for id in os.environ.get("OWNER_ID", '').split()]
    BOT_OWNER_ID = [int(id) for id in os.environ.get("BOT_OWNER_ID", '').split()]
    UPDATES_CHANNEL = ""

class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
    

