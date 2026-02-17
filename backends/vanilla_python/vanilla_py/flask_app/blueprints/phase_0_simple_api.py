from flask_cors import CORS
from flask import Blueprint, jsonify


simple_api = Blueprint('simple_api', __name__, template_folder='templates')

@simple_api.route('hello')
def hello():
    payload = {
            "content" : "hello world",
            "status" : 200
        }
    return jsonify(payload), 200

@simple_api.get('/hello_restful/<int:fake_password>')
def hello_restful(fake_password):

    is_good  =  fake_password > 10   
    
    if not is_good :
        return jsonify({
            "content" : "you are using restful, but the pass word is not right",
            "reason" : "enter a number smaller than 10"    
        }), 401
    else :
        return jsonify({
            "content" : "you are using restful",
            "reason" : "All is good"  
        }), 200
    
    return payload