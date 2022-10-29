from flask import Flask
from flask import render_template
from datetime import datetime
from flask import request
import random
import string
import json
from flask import jsonify


import requests
import json
from tinydb import TinyDB, Query
import pprint
import argparse


app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT']=0
chat_id = 1
chats = {
     "1": {
         "creator": "session_token_0",
         "authorized_users": {
             "session_token_0": {"username": "Alice", "expires": "2020-02-15T20:53:15Z"},
             "session_token_1": {"username": "Bob", "expires": "2020-02-15T20:57:22Z"}
         },
         "magic_key": "some_really_long_key_value",
         "messages": [
             {"username": "Alice", "body": "Hi Bob!"},
             {"username": "Bob", "body": "Hi Alice!"},
             {"username": "Alice", "body": "Knock knock"},
             {"username": "Bob", "body": "Who's there?"},
         ]
     }
}

mediator_addr = "http://127.0.0.1:6666/"
headers = {'Content-Type':'application/json'}

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/api/login", methods = ['POST'])
def login():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    dummy_item = {'email':data['email'], 'password':data['password']}
    r= requests.post(mediator_addr + "login", data=json.dumps(dummy_item),headers=headers)
    print(r.json())
    return jsonify(r.json())

@app.route("/api/logout", methods = ['POST'])
def logout():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    dummy_item = {'id':data['id']}
    r= requests.post(mediator_addr + "logout", data=json.dumps(dummy_item),headers=headers)
    print(r.json())
    return jsonify(r.json())

@app.route("/api/register", methods = ['PUT'])
def register():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    dummy_item = {'email':data['email'], 'password':data['password']}
    r= requests.put(mediator_addr + "create_user", data=json.dumps(dummy_item),headers=headers)
    print(r.json())
    return jsonify(r.json())

@app.route("/main_page")
def main_page():
    return render_template("main_page.html")


@app.route("/api/add_item", methods = ['PUT'])
def add_item():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    dummy_item = {'name':data['name'], 'start_time':data['start_time'], 
                  'end_time':data['end_time'], 'category':data['category'],
                  'start_bidding_price':data['start_bidding_price'], 'buyout_price':data['buyout_price'], 
                  'user_key':data['user_key']}
    r= requests.post(mediator_addr + "create_item_for_user/" + data['user_key'], data=json.dumps(dummy_item),headers=headers)
    print(r.json())
    return jsonify(r.json())

@app.route("/api/get_auction_items_by_category", methods = ['POST'])
def search_item_category():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    r= requests.get(mediator_addr + "get_auction_items_by_category/" + data['category'], headers=headers)
    print(r.json())
    return jsonify(r.json())

@app.route("/api/get_auction_items_by_keyword", methods = ['POST'])
def search_item_keyword():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    r= requests.get(mediator_addr + "get_auction_items_by_keyword/" + data['keyword'], headers=headers)
    print(r.json())
    return jsonify(r.json())



@app.route("/api/update_item_for_user", methods = ['POST'])
def modify_item():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    dummy_item = {'name':data['name'], 'start_time':data['start_time'], 
                  'end_time':data['end_time'], 'category':data['category'],
                  'start_bidding_price':data['start_bidding_price'], 'buyout_price':data['buyout_price'], 
                  'user_key':data['user_key']}
    r= requests.post(mediator_addr + "update_item_for_user/" + str(data['user_key']) + "/" + str(data['item_key']), data=json.dumps(dummy_item),headers=headers)
    print(r.json())
    return jsonify(r.json())

@app.route("/api/remove_item_for_user", methods = ['POST'])
def delete_item():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    dummy_item = {'item_key':data['item_key']}
    r= requests.post(mediator_addr + "remove_item_for_user/" + str(data['user_key']) + "/" + str(data['item_key']), data=json.dumps(dummy_item),headers=headers)
    print(r.json())
    return jsonify(r.json())


@app.route("/api/get_all_auction_items", methods = ['GET'])
def get():
    print("get auction items")
    r= requests.get(mediator_addr + "get_all_auction_items", headers=headers)
    print(r.json())
    return jsonify(r.json())


@app.route("/api/get_auction_items_by_user", methods = ['POST'])
def get_my():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    r= requests.get(mediator_addr + "get_auction_items_by_user/" + str(data['id']), headers=headers)
    print(r.json())
    return jsonify(r.json())

@app.route("/api/update_email", methods = ['POST'])
def update_email():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    dummy_item = {'email':data['email'], 'id':data['id']}
    r= requests.post(mediator_addr + "update_email", data=json.dumps(dummy_item),headers=headers)
    print(r.json())
    return jsonify(r.json())

@app.route("/api/update_password", methods = ['POST'])
def update_password():
    print(request.data.decode())
    data = json.loads(request.data.decode())
    dummy_item = {'password':data['password'], 'id':data['id']}
    r= requests.post(mediator_addr + "update_password", data=json.dumps(dummy_item),headers=headers)
    print(r.json())
    return jsonify(r.json())
























@app.route("/create")
def create_chat():
    if "magic_key" in request.args :
        print("join chat"+request.args["magic_key"])
        for chat in chats.items():
            if request.args["magic_key"] == chat[1]["magic_key"]:
                return render_template("chat_project.html", chat_id = chat[0], magic_key = request.args["magic_key"])
    return render_template("chat_project.html")



@app.route("/api/create", methods = ['POST'])
def create():

    print(request.data.decode())
    global chat_id
    chat_id = chat_id + 1

    session_token = randomString(30)
    magic_key = randomString(30)
    magic_invite_link = "http://localhost:5000/?magic_key=" + magic_key
    username = request.data.decode()

    chat = {
         "creator": session_token,
         "authorized_users": {
             session_token: {"username": username, "expires": "2020-02-15T20:53:15Z"},
         },
         "magic_key": magic_key,
         "messages": [

         ]
     }

    chats[str(chat_id)] = chat
    return {
        "chat_id":str(chat_id),
        "session_token":session_token,
        "magic_invite_link": magic_invite_link
    }

@app.route("/api/<this_chat_id>/invite", methods = ['POST'])
def invite(this_chat_id):
    session_token = request.headers["session_token"]
    magic_link = ""

    if(int(this_chat_id) <= chat_id):
        if(session_token == chats[this_chat_id]["creator"]):
            magic_link = "http://localhost:5000/?magic_key="+chats[this_chat_id]["magic_key"]
    return magic_link

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    # TODO: check if the request body contains a chat_id and the correct magic_key for that chat
    # TODO: also send a username
    print(request.data)

    data = json.loads(request.data.decode())
    session_token = ""

    if("chat_id" in data):
        chat_id = data["chat_id"]
        chat = chats[chat_id]
        if("magic_key" in data):
            magic_key = chat["magic_key"]
            if(data["magic_key"] == magic_key):
                session_token = randomString(30)
                chat["authorized_users"][session_token] = {"username": data["username"]}

    return session_token

@app.route('/api/messages', methods=['GET', 'POST'])
def messages ():
    # TODO: check if the request body contains a chat_id and valid session token for that chat
    print(request.data)
    print(request.headers["username"])
    headers = request.headers

    if(int(headers["chat_id"]) > chat_id):
        print("chat room id not correct")
        return "{}"
    if headers["session_token"] not in chats[headers["chat_id"]]["authorized_users"].keys():
        print(chats[headers["chat_id"]]["authorized_users"].keys())

        print(headers["session_token"])
        return "{}"

    if request.method == 'POST':
        # TODO: add the message
        data = json.loads(request.data.decode())
        print(data)

        new_message = {"username": headers["username"], "body": data["message"]}
        chats[headers["chat_id"]]["messages"].append(new_message)

    # TODO: get the messages for this chat from global memory

    print(chats[headers["chat_id"]]["messages"])
    return {
        "messages": chats[headers["chat_id"]]["messages"],
    }

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


