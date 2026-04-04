
from flask  import CORS
from flask import BluePrint, jsonify, request
from .. import db
from werkzeug.security import check_password_hash, generate_password_hash
import datetime 

## Setting up the Blue Print 
phase_1_bp  = BluePrint('auth', __name__, url_prefix='/phase_1_bp')
## User Authentication Simplified!
@phase_1_bp.get ('/type_0_authentication')
def type_0_authentication():
    #For simple  authentication, just expect only the user name and password

    # Connect with the database
    database = db.get_db()
    
    payload = {
        "login_success" : True,
        "message" : "",
        "user_uuid" : "" 
    }
    
    data = request.get_json()
    
    user_name  = data.get("use_name")
    password = data.get("password")
    try:
        user_res = database.execute("SELECT * FROM users WHERE username= ? AND password= ? ", (user_name,password  ))
        if user_res.fetchone() is None :
            payload["login_success"] = False
            payload["message"] = "User Does Not Exist or Password not correct"
            payload["uuid"] ="NONE"
            
            return jsonify(payload), 400
        else:
            payload["login_success"] = True
            payload["message"] = "User Exist, Log In successful, but do use this in a real case"
            #if the use exist, then extract  the uuid
            #assume the user found is unique
            payload["uuid"] = user_res[0]
           
            return  jsonify(payload), 200
    except Exception as e:
        print(e) 
    finally:
        database.close()

@phase_1_bp.get('/type_1_authentication')
def type_1_authentication():
    #frontend still sends username and password
    #backend still looks up the user by username
    #but the database stores password_hash, not the raw password
    #backend does not compare password directly in SQL
    #backend loads the user row first, then checks the password using a hash-checking function
    
    database =db.get_db()
    payload = {
        "login_success" : True,
        "message" : "",
        "user_uuid" : "" 
    }
    data = request.get_json()
    
    user_name  = data.get("use_name")
    password = data.get("password")

    
    try:
        hashedPassWord = database.execute("SELECT * FROM users WHERE  username = ?", (user_name))
        if hashedPassWord.fetchone() is None :
            payload["login_success"] = False
            payload["message"] = "User Does Not Exist or t he Password Wrong (hush its actually the User does not exist)"
            payload["uuid"] ="NONE"
            return jsonify(payload), 400
        else:
            if check_password_hash(hashedPassWord[2], password):
                payload["login_success"] = True
                payload["message"] = "Log In successful"
                #if the use exist, then extract  the uuid
                #assume the user found is unique
                payload["uuid"] = hashedPassWord[0]
                '''
                    Maybe also here is the place to set the is active status?
                '''
                return jsonify(payload), 200
            else:
                payload["login_success"] = False
                payload["message"] = "User Does Not Exist or t he Password Wrong (hush its actually the password not right)"
                #if the use exist, then extract  the uuid
                #assume the user found is unique
                payload["uuid"] = hashedPassWord[0]
                return jsonify(payload), 400
    except Exception as e:
        print(e) 
    finally:
        database.close()

@phase_1_bp.post('/type_1_user_registering')
def type_1_user_registering():
    '''
    Docstring for type_1_user_registering
        ##  Receive the user name and password
        ##  Check for use uniqueness
        ##  Hash the pass word
        ##  Store in the Data Base 
        ##  Return Success
    '''   
    payload = {
        "signup_success" : True,
        "message" : "",
        "user_uuid" : "" 
    }
    ## Connect o DB

    database  =db.get_db()

    ## Receive the frontend request

    new_usr  = request.get_json()
    user_name  = new_usr.get("user_name")
    password = new_usr.get("password")
    role = new_usr.get("role")
    gender = new_usr.get("gender")
    left_right_hand = new_usr.get("hand")



    ## Check if user exist already?

    try :
        if (database.execute("SELECT * FROM users WHERE  username = ?", (user_name,)).fetchone() is None) :
            database.commit()
            pass
        else :
            payload["message"] = f"{user_name} is already register"
            payload["signup_success"] = False          
            return jsonify(payload), 400
    except Exception as e:
        payload["message"] = f"{str(e)}"
        payload["signup_success"] = False
        print(e)
        return jsonify(payload), 400
    
    ## If exist then return False 
    ## If does not exist, insert into the database
    ## also encrypt the password.
    
    try :
        hashed_password  = generate_password_hash(password)
        database.execute("""INSERT INTO users(id, username, password, creation_date, role, gender, left_right_handed)
                          VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                (str(uuid.uuid4()), user_name, hashed_password, 
                 datetime.datetime.now(), role, gender,left_right_hand)
        )
        payload["message"] = "Sign Up Successful"
        payload["signup_success"] = True
        return  jsonify(payload), 200

    except Exception as e:
        payload["message"] = f"{str(e)}"
        payload["signup_success"] = False
        return jsonify(payload), 400 


@phase_1_bp.post('/type_2_authentication')
def type_2_authentication():
    payload = {
        "login_success" : True,
        "message" : "",
        "user_session" : "",
        "uuid" :""
    }
    session_live_time = 30
    database  = db.get_db()
    user_info = request.get_json()
    user_name = user_info.get("user_name")
    password = user_info.get("password")

    
    try:
        hashedPassWord = database.execute("SELECT * FROM users WHERE  username = ?", (user_name,))
        if hashedPassWord.fetchone() is None :
            payload["login_success"] = False
            payload["message"] = "User Does Not Exist or t he Password Wrong (hush its actually the User does not exist)"
            payload["uuid"] ="NONE"
            return jsonify(payload), 400
        else:
            if check_password_hash(hashedPassWord.fetchone()[2], password):
                payload["login_success"] = True
                payload["message"] = "Log In successful"
                #if the use exist, then extract  the uuid
                #assume the user found is unique
                payload["uuid"] = hashedPassWord.fetchone()[0]

                # Give a session for the user
                session_uuid = str(uuid.uuid4())
                session_id  = str(uuid.uuid4())
                created_at  = str(datetime.datetime.now())
                expire_at  = str(datetime.datetime.now()+datetime.timedelta(minutes=session_live_time))
                try:
                    database.execute('''
                        INSERT INTO sessions(uuid, session_id,user_id, created_at, expires_at, isValid)
                        VALUES(?, ?, ?, ?, ?, ?) 
                    ''', (session_uuid, session_id, hashedPassWord[0], created_at, expire_at, 1))
                    database.commit()
                except Exception as e:
                    payload["login_success"] = False
                    payload["message"] = "Failed to create session"
                    payload["uuid"] = hashedPassWord[0]
                    return  jsonify(payload), 400

                payload["user_session"] = session_id
                # Return the session
                # Return the session as cookies ( always a backend job) 
                response = jsonify(payload)
                response.set_cookie(
                    "session_id",
                    session_id,
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    max_age=30 * 60
                )
                return response, 200
            else:
                payload["login_success"] = False
                payload["message"] = "User Does Not Exist or t he Password Wrong (hush its actually the password not right)"
                #if the use exist, then extract  the uuid
                #assume the user found is unique
                payload["uuid"] = hashedPassWord[0]
                return jsonify(payload), 400
    except Exception as e:
        print(e)
        payload["login_success"] = False
        payload["message"] = "Internal server error"
        return jsonify(payload), 500
         
    finally:
        database.close()


@phase_1_bp.post('type_2_user_signup')
def type_2_user_signup():
    # Connect with the database
    database  = db.get_db()
    payload = {
        "login_success" : True,
        "message" : "",
        "uuid" :""
    }
    # Receive the request from the frontend 
    data  = request.get_json()

    user_name = data.get("user_name")
    password  = data.get("password")
    role = data.get("role")
    gender = data.get("gender")
    left_right_hand = data.get("hand")
    
    # Check if user exit in the user data base 
    try :
        user_res  = database.execute("SELECT * FROM users WHERE username= ? ",
                                     (user_name,))
        if user_res.fetchone() is None:
            # User name is new, go a head with the user registration
            try :
                # Generate a hashed password
                hashed_password = generate_password_hash(password)
                uuid  = str(uuid.uuid4())
                database.execute("""INSERT INTO users(id, username, password, creation_date, role, gender, left_right_handed)
                          VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                (uuid, user_name, hashed_password, 
                 datetime.datetime.now(), role, gender,left_right_hand))
                database.commit()
                # Also return user a session, save the session into a database 
                session_uuid = str(uuid.uuid4())
                session_id  = str(uuid.uuid4())
                created_at  = str(datetime.datetime.now())
                expire_at  = str(datetime.datetime.now()+datetime.timedelta(minutes=30))
                try:
                    database.execute('''
                        INSERT INTO sessions(uuid, session_id,user_id, created_at, expires_at, isValid)
                        VALUES(?, ?, ?, ?, ?, ?) 
                    ''', (session_uuid, session_id, hashed_password, created_at, expire_at, 1))
                    database.commit()
                except Exception as e:
                    payload["login_success"] = False
                    payload["message"] = "Failed to create session for the new user "
                    return  jsonify(payload), 400
                
                # Set the payload object
                payload ["login_success"] = True
                payload ["message"] = "Account created successfully"
                payload ["uuid"] = uuid
                # Set response, set session cookies
                response = jsonify(payload)
                response.set_cookie(
                    "session_id",
                    session_id,
                    httponly=True,
                    secure=True,
                    samesite="Lax",
                    max_age=30 * 60
                )
                return response, 200
            except Exception as e:
                payload ["login_success"] = False
                payload ["message"] = "Account created successfully"
                payload ["uuid"] = ""
                return  jsonify(payload), 200 
        else:
            # User name already exist, return false
            payload ["login_success"] = False
            payload ["message"] = "Account name already exist"
            payload ["uuid"] = ""
            return  jsonify(payload), 200 
    except Exception as e:
        payload["message"] = "Failed to Create user due to unexpected error"
        return jsonify(payload), 400 
    
@phase_1_bp.get('/type_3_authentication')
def type_3_authentication():
    return  0

@phase_1_bp.get("/type_3_create_user")
def type_3_user_creation():

    # The user creation does not return a token to the user when the creation is done.
    payload = {
        "login_success" : True,
        "message" : "",
    }
    data = request.get_json()
    database = db.get_db()
    user_name  =data.get("user_name")
    user_password = data.get("password")
    role = data.get("role")
    gender = data.get("gender")
    left_right_hand = data.get("hand")

    # Check if user exist  
    try:
        user_res  = database.execute("SELECT * FROM users WHERE username= ? ",
                                     (user_name,))
        if user_res.fetchone() is None:
            # User name is new, the go ahead with user creation

            try:
                # Generate a hashed password 
                hashed_password = generate_password_hash(user_password)
                uuid  = str(uuid.uuid4())
                database.execute("""INSERT INTO users(id, username, password, creation_date, role, gender, left_right_handed)
                          VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                (uuid, user_name, hashed_password, 
                 datetime.datetime.now(), role, gender,left_right_hand))
                database.commit()
                payload["login_success"] = True
                payload["message"] = "everything is good"

                return  jsonify(payload), 200
            except Exception as e:
                payload["login_success"] = False
                payload["message"] = "user creation failed"
                return  jsonify(payload), 400
    except Exception as e:
        payload["login_success"] = False 
        payload["message"] = "user creation failed"
        return jsonify(payload), 400
    
    return 0

