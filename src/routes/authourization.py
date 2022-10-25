from flask import request,Blueprint,jsonify
from ..database.models import User
from flask_jwt_extended import create_access_token
import datetime

auth = Blueprint("auth",__name__,url_prefix='/api/v1/auth')

@auth.post('/signup')
def sign_up():
    body = request.get_json()
    user = User(**body)
    user.hash_password()
    user.save()
    id = user.id
    return jsonify({"id":str(id)})

@auth.post('/login')
def user_login():
    body = request.get_json()
    user = User.objects.get(email=body.get('email'))
    authorized = user.check_password(password=body.get('password'))
    
    if not authorized:
        return jsonify({"success": False,"msg":"Invalid email or password"}),401
    
    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    return jsonify({"token":access_token})