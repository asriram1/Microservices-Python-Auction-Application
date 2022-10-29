from admin_DB import *
from flask import Flask, jsonify, request, make_response, render_template, session, redirect, url_for

app = Flask(__name__)

admin_db = Admin_DB()

# @app.route("/", methods = ['GET'])
# def homepage():
#     return "test"

@app.route('/admin/sign_up', methods=['POST'])
def admin_sign_up():
    try:
        req_data = request.get_json()
    except:
        print('didnt get data')
        raise

    if not req_data:
        return jsonify({"Error":"No parameters provided"}),400

    try:
        username = req_data['username']
        password = req_data['password']
    except:
        print('wrong username')
        raise

    try:
        admin_db.signup(username, password)
        return "Success"
    except:
        return jsonify({"Reason":"Username already exists"}),400
    
@app.route('/admin/login', methods=['POST'])
def admin_login():
    try:
        req_data = request.get_json()
    except:
        raise

    if not req_data:
        return jsonify({"Error":"No parameters provided"}),400
    try:
        username = req_data['username']
        password = req_data['password']
    except:
        raise

    try:
        admin_db.login(username,password)
        return "Success"
    except:
        return jsonify({"Error":"Incorrect username or password"}),400
        

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    try:
        req_data = request.get_json()
    except:
        raise

    if not req_data:
        return jsonify({"Error":"No parameters provided"}),400
    try:
        username = req_data['username']
    except:
        raise
    try:
        admin_db.logout(username)
        return "Success"
    except:
        return jsonify({"Error":"Admin already logged out"}),400



@app.route('/admin/username_change', methods=['POST'])
def admin_username_change():
    try:
        req_data = request.get_json()
    except:
        raise

    if not req_data:
        return jsonify({"Error":"No parameters provided"}),400
    try:
        old_username = req_data['old_username']
        new_username = req_data['new_username']
    except:
        raise

    try:
        admin_db.change_admin_username(new_username,old_username)
        return "Success"
    except:
        return jsonify({"Error":"An unexpected error occurred"}),400


if __name__ == '__main__':
    app.run(debug=True)



