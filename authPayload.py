from datetime import datetime  
from datetime import timedelta  
import os

class authPayload(dict):

    def __init__(self, id, email,admin):

        EXPIRESSECONDS = 3000

        # set the id of the object from Postgres
        self.id = id

        #  The client id (like the user id)
        self.email = email

        self.admin = admin

        # set the expiry attrbute to 30 minutes
        self.exp = datetime.utcnow() + timedelta(seconds=EXPIRESSECONDS)