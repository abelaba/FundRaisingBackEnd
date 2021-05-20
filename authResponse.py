class authResponse(dict):
    
    def __init__(self, token, expiresin):
        self.token = token
        self.expiresin = expiresin