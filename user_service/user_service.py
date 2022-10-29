from flask import Flask, request, jsonify
from class_types import User, Acknowledgement_base, Endpoint, User_Ack
from tinydb import TinyDB, Query, where
import json
import requests

app = Flask(__name__)

users_db = TinyDB('users.json')

endpoints = {}
headers = {'Content-Type':'application/json'}
with open("endpoints.json") as endpoints_config:
    data = json.load(endpoints_config)
    for idx,ep in enumerate(data['services']):
        endpoints[ep['domain']] = Endpoint(ep['domain'],ep['ip'],ep['port'])

@app.route("/create_user", methods=['PUT'])
def create_user():
    User = Query()
    results = users_db.search(User['email'] == request.json['email'])
    if (len(results)) != 0:
        return jsonify(Acknowledgement_base(False).serialize()), 500
    else:
        users_db.insert({'email': request.json['email'], 'password': request.json['password'],
                         'login': False, 'suspend': False, 'items': []})
        return jsonify(Acknowledgement_base(True).serialize()), 200

@app.route('/login', methods=['POST'])
def login():
    User = Query()
    results = users_db.search((User['email'] == request.json['email']) &
                              (User['password'] == request.json['password']) &
                              (User['suspend'] == False))
    if len(results) == 1:
        id = results[0].doc_id
        users_db.update({'login': True}, doc_ids=[id])
        return jsonify(User_Ack(True, id).serialize()), 200
    else:
        return jsonify(Acknowledgement_base(False).serialize()), 404

@app.route('/logout', methods=['POST'])
def logout():
    users_db.update({'login': False}, doc_ids=[request.json['id']])
    return jsonify(Acknowledgement_base(True).serialize()), 200

@app.route('/update_email', methods=['POST'])
def update_email():
    users_db.update({'email': request.json['email']}, doc_ids=[request.json['id']])
    return jsonify(Acknowledgement_base(True).serialize()), 200

@app.route('/update_password', methods=['POST'])
def update_password():
    users_db.update({'password': request.json['password']}, doc_ids=[request.json['id']])
    return jsonify(Acknowledgement_base(True).serialize()), 200

@app.route('/suspend', methods=['POST'])
def suspend():
    users_db.update({'suspend': True}, doc_ids=[request.json['id']])
    return jsonify(Acknowledgement_base(True).serialize()), 200

@app.route('/unblock', methods=['POST'])
def suspend():
    users_db.update({'suspend': False}, doc_ids=[request.json['id']])
    return jsonify(Acknowledgement_base(True).serialize()), 200

@app.route('/remove_account', methods=['POST'])
def remove_account():
    users_db.remove(doc_ids=[request.json['id']])
    return jsonify(Acknowledgement_base(True).serialize()), 200

@app.route('/create_item_for_user/<int:user_key>', methods=['POST'])
def create_item_for_user(user_key):
    r = requests.put(endpoints['mediator'].get_prefix() + "create_auction_item", data=json.dumps(request.json),headers=headers)
    record = users_db.get(doc_id=user_key)
    new_items = record['items']
    new_items.append(r.json()['item_key'])
    users_db.update({'items': new_items}, doc_ids=[user_key])
    return jsonify(Acknowledgement_base(True).serialize()), 200

@app.route('/update_item_for_user/<int:user_key>/<int:item_key>', methods=['POST'])
def update_item_for_user(user_key, item_key):
    r = requests.put(endpoints['mediator'].get_prefix() + "update_auction_item/" + str(item_key), data=json.dumps(request.json),headers=headers)
    return jsonify(Acknowledgement_base(r.json()['success']).serialize()), 200

@app.route('/remove_item_for_user/<int:user_key>/<int:item_key>', methods=['POST'])
def remove_item_for_user(user_key, item_key):
    r = requests.put(endpoints['mediator'].get_prefix() + "remove_auction_item/" + str(item_key), data=json.dumps(request.json), headers=headers)
    
    if r.json()['success'] == False:
        return jsonify(Acknowledgement_base(False).serialize()), 404
    
    record = users_db.get(doc_id=user_key)
    new_items = record['items']
    if (r.json()['item_key'] in new_items):
        new_items.remove(r.json()['item_key'])
        users_db.update({'items': new_items}, doc_ids=[user_key])
        return jsonify(Acknowledgement_base(True).serialize()), 200
    else:
        jsonify(Acknowledgement_base(False).serialize()), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6662, debug=True)
