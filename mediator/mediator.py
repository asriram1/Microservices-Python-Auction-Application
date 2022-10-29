from flask import Flask,request,jsonify
from class_types import Item_base, Acknowledgement_base, Endpoint, User
from tinydb import TinyDB, Query
import requests
import json
import pprint
import argparse
import pika

app = Flask(__name__)
endpoints = {}
headers = {'Content-Type':'application/json'}
with open("endpoints.json") as endpoints_config:
    data = json.load(endpoints_config)
    for idx,ep in enumerate(data['services']):
        endpoints[ep['domain']] = Endpoint(ep['domain'],ep['ip'],ep['port'])

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='email_queue')


APIBaseURL = 'http://127.0.0.1:6663'
endpointdict = {
        'admin_login': f'{APIBaseURL}/admin/login',
        'admin_signup': f'{APIBaseURL}/admin/sign_up',
        'admin_logout': f'{APIBaseURL}/admin/logout',
        'admin_changeusername': f'{APIBaseURL}/admin/username_change'
    }

# front end (user login) can directly this to bid an item, 3 fields need to be provoded from json
# item_key , user_key, bid_price
@app.route("/bid_item", methods=['PUT'])
def bid_item():
    r=requests.put(endpoints['auction'].get_prefix() + "bid_item", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

#only user_service should call create_auction_item
# request json should have append the following fields attached:
# ['name']
# ['start_time']
# ['end_time']
# ['category']
# ['start_bidding_price']
# ['buyout_price']
# ['user_key']
@app.route("/create_auction_item", methods=['PUT'])
def create_auction_item():
    r=requests.put(endpoints['auction'].get_prefix() + "create_auction_item", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# only user/admin service should call update_auction_item
@app.route("/update_auction_item/<int:key>", methods=['PUT'])
def update_auction_item(key):
    r=requests.put(endpoints['auction'].get_prefix() + "update_auction_item/"+str(key), data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# only user/admin service should call remove_auction_item, can only be removed if an item hasn't started auction
@app.route("/remove_auction_item/<int:key>", methods=['PUT'])
def remove_auction_item(key):
    r=requests.put(endpoints['auction'].get_prefix() + "remove_auction_item/"+str(key), headers=headers)
    return jsonify(r.json())

# fronend can directly call get_all_auction_items either for user or admin, return all items that currectly in 'started' auction state
@app.route("/get_all_auction_items", methods=['GET'])
def get_all_auction_items():
    r=requests.get(endpoints['auction'].get_prefix() + "get_all_auction_items", headers=headers)
    return jsonify(r.json())

# frontend user/admin should call get_auction_items_by_category to get details of items of one category
# category field should only contain alphabet letters or numbers, no special charactor(such as space) allowed.
#returning items are all currectly in 'started' auction state
@app.route("/get_auction_items_by_category/<string:category>", methods=['GET'])
def get_auction_items_by_category(category):
    r=requests.get(endpoints['auction'].get_prefix() + "get_auction_items_by_category/" + category, headers=headers)
    return jsonify(r.json())

# only user/admin service should call get_auction_items_by_key to get details of an item
@app.route("/get_auction_items_by_key/<string:item_key>", methods=['GET'])
def get_auction_items_by_key(item_key):
    r=requests.get(endpoints['auction'].get_prefix() + "get_auction_items_by_key/" + item_key, headers=headers)
    return jsonify(r.json())

# expose to frontend user/admin
#returning items are all currectly in 'started' auction state
@app.route("/get_auction_items_by_keyword/<string:keyword>", methods=['GET'])
def get_auction_items_by_keyword(keyword):
    r=requests.get(endpoints['auction'].get_prefix() + "get_auction_items_by_keyword/" + keyword, headers=headers)
    return jsonify(r.json())

# expose to frontend user/admin
@app.route("/get_auction_items_by_user/<string:user_key>", methods=['GET'])
def get_auction_items_by_user(user_key):
    r=requests.get(endpoints['auction'].get_prefix() + "get_auction_items_by_user/" + user_key, headers=headers)
    return jsonify(r.json())

# front end can directly call create user, return 200 or 404
@app.route("/create_user", methods=['PUT'])
def create_user():
    r=requests.put(endpoints['user'].get_prefix() + "create_user", data=json.dumps(request.json), headers=headers)
    return jsonify(r.json())

# only frontend user can call login, return 200 or 404
@app.route('/login', methods=['POST'])
def login():
    r=requests.post(endpoints['user'].get_prefix() + "login", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# only frontend user can call logout, return 200
@app.route('/logout', methods=['POST'])
def logout():
    r=requests.post(endpoints['user'].get_prefix() + "logout", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# only frontend user or admin can call update_email, return 200
@app.route('/update_email', methods=['POST'])
def update_email():
    r=requests.post(endpoints['user'].get_prefix() + "update_email", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# only frontend user or admin can call update_password, return 200
@app.route('/update_password', methods=['POST'])
def update_password():
    r=requests.post(endpoints['user'].get_prefix() + "update_password", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# frontend user and admin can call suspend, return 200
@app.route('/suspend', methods=['POST'])
def suspend():
    r=requests.post(endpoints['user'].get_prefix() + "suspend", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# frontend user and admin can call remove_account, return 200
@app.route('/remove_account', methods=['POST'])
def remove_account():
    r=requests.post(endpoints['user'].get_prefix() + "remove_account", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# frontend user can call create_item_for_user and it will return acknowledgement
@app.route('/create_item_for_user/<int:user_key>', methods=['POST'])
def create_item_for_user(user_key):
    r=requests.post(endpoints['user'].get_prefix() + "create_item_for_user/" + str(user_key), data=json.dumps(request.json), headers=headers)
    return jsonify(r.json())

# frontend user can call update_item_for_user and it will return acknowledgement
@app.route('/update_item_for_user/<int:user_key>/<int:item_key>', methods=['POST'])
def update_item_for_user(user_key, item_key):
    r=requests.post(endpoints['user'].get_prefix() + "update_item_for_user/" + str(user_key) + "/" + str(item_key), data=json.dumps(request.json), headers=headers)
    return jsonify(r.json())

# frontend user can remove_item_for_user and it will return acknowledgement
@app.route('/remove_item_for_user/<int:user_key>/<int:item_key>', methods=['POST'])
def remove_item_for_user(user_key, item_key):
    r=requests.post(endpoints['user'].get_prefix() + "remove_item_for_user/" + str(user_key) + "/" + str(item_key), data=json.dumps(request.json), headers=headers)
    return jsonify(r.json())

# admin sign up
@app.route('/admin/sign_up', methods=['POST'])
def admin_signup():
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']
    r = requests.post(endpointdict['admin_signup'], json={'username': username, 'password': password})
    return "Successful admin sign up"

# admin login
@app.route('/admin/login', methods=['POST'])
def admin_login():
    req_data = request.get_json()
    username = req_data['username']
    password = req_data['password']
    r = requests.post(endpointdict['admin_login'], json={'username': username, 'password': password})
    return "Successful admin login"

# admin logout
@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    req_data = request.get_json()
    username = req_data['username']
    r = requests.post(endpointdict['admin_logout'], json={'username': username})
    return "Successful admin logout"

# admin change username
@app.route('/admin/username_change', methods=['POST'])
def admin_changeusername():
    req_data = request.get_json()
    try:
        old_username = req_data['old_username']
        new_username = req_data['new_username']
    except:
        print("No data")
    try:
        r = requests.post(endpointdict['admin_changeusername'],
                                json={'old_username': old_username, 'new_username': new_username})
    except:
        print("Couldn't post")
    return "Successfully changed admin username"

@app.route('/admin/remove_user', methods = ['POST'])
def admin_remove_user():
    r=requests.post(endpoints['user'].get_prefix() + "remove_account", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

@app.route('/admin/block_user', methods = ['POST'])
def admin_block_user():
    r=requests.post(endpoints['user'].get_prefix() + "suspend", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

@app.route('/admin/unblock_user', methods = ['POST'])
def admin_unblock_user():
    r=requests.post(endpoints['user'].get_prefix() + "unblock", data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

@app.route('/admin/send_email', methods = ['POST'])
def admin_send_email():
    channel.basic_publish(exchange='',routing_key='email_queue',body=json.dumps(request.json))
    return jsonify({'success':True})

@app.route('/admin/modify_category', methods = ['POST'])
def admin_modify_category():
    r=requests.put(endpoints['auction'].get_prefix() + "update_auction_item/"+str(key), data=json.dumps(request.json),headers=headers)
    return jsonify(r.json())

# backend user/admin service calling this api should append json with 3 fields:
# 'to':<dest email addr>
# 'subject':<email subject>
# 'body' : <email body>
@app.route('/send_email', methods=['POST'])
def send_email():
    channel.basic_publish(exchange='',routing_key='email_queue',body=json.dumps(request.json))
    return jsonify({'success':True})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6666, debug=True)
