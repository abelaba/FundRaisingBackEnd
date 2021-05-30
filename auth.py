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



@app.route("/addFund",methods=["POST"])
def addFund():
    vertification = authModel.verify(request.form.get("token"))
    userId =  vertification["id"]
    fundTitle = request.form.get("title")
    fundCategory = request.form.get("category")
    fundDescription =  request.form.get("descr")
    fundGoal =  request.form.get("Goal")
    addRes = crudModel.newFund(userId,fundTitle,fundCategory,fundDescription,fundGoal)
    return {'success':addRes}
@app.route('/getFunds', methods=["GET"])
def getFunds():
    Funds =  crudModel.getFunds()
    return Funds
@app.route('/delete',methods=["POST"])
def deleteFunds():
    vertification = authModel.verify(request.form.get("token"))
    fundId =  request.form.get("fundId")
    userId = vertification["id"]
    if userId:
        result = crudModel.deleteFunds(fundId,userId)
        return result
    else:
        return False
@app.route('/pay',methods=["POST"])
def pay():
    c_id = int(request.form.get("cid"))
    amount = int(request.form.get("amount"))
    name = request.form.get("name")
    card = request.form.get("card")
    expiry = request.form.get("expiry")
    cvv = request.form.get("cvv")
    result = crudModel.pay(c_id,amount,name,card,expiry,cvv)
    return {"success":result}
@app.route('/withdraw', methods=["POST"])
def withdraw():
    amount = int(request.form.get("amount"))
    account = request.form.get("account")
    userId = request.form.get("id")
    result = crudModel.withdraw(userId,account,amount)
    return {"success":result}