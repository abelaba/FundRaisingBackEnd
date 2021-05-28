from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import hashlib
import authModel
import crudModel
import jwt
import json
AUTHSECRET = "keyboardcat"
# instantiate the Flask app.
app = Flask(__name__)
cors = CORS(app)
app.config['Access-Control--AllowOrigin'] = '*'

# API Route for checking the client_id and client_secret
@app.route("/auth", methods=["POST"])
def auth():	
    # get the client_id and secret from the client application
    email = request.form.get("email")
    password_input = request.form.get("password")
  
    # the client secret in the database is "hashed" with a one-way hash
    hash_object = hashlib.sha1(bytes(password_input, 'utf-8'))
    hashed_password = hash_object.hexdigest()

    # make a call to the model to authenticate
    authentication = authModel.authenticate(email, hashed_password)
    if authentication == False:
        return {'success': False}
    else: 
        return json.dumps(authentication)

# API route for verifying the token passed by API calls
@app.route("/verify", methods=["POST"])
def verify():
    # verify the token 
    token = request.json["token"]
    verification = authModel.verify(token)
    return verification

@app.route("/Newuser", methods=["POST","DELETE"])
def client():
    if request.method == 'POST':

        # verify the token 
        # authorizationHeader = request.headers.get('authorization')	
        # token = authorizationHeader.replace("Bearer ","")
        # verification = authModel.verify(token)
        
        
        # get the email and password from font end 
        email = request.form.get("email")
        username = request.form.get("username")

        password_input = request.form.get("password")
        
        # the client secret in the database is "hashed" with a one-way hash
        hash_object = hashlib.sha1(bytes(password_input, 'utf-8'))
        hashed_password = hash_object.hexdigest()

            # make a call to the model to authenticate
        createResponse = authModel.create(email, username, hashed_password)
        return {'success': createResponse}
         
        
    elif request.method == 'DELETE':
        # not yet implemented
        return {'success': False}
    else:        
        return {'success': False}