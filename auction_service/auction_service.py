from flask import Flask,request,jsonify
from class_types import Item_base, Acknowledgement_base, Item_Auction, Item_Ack, Endpoint
from tinydb import TinyDB, Query, where
import re
from datetime import datetime
import time
import json
import requests
import threading


app = Flask(__name__)
endpoints = {}
with open("endpoints.json") as endpoints_config:
    data = json.load(endpoints_config)
    for idx,ep in enumerate(data['services']):
        endpoints[ep['domain']] = Endpoint(ep['domain'],ep['ip'],ep['port'])
items_db = TinyDB('items.json')

headers = {'Content-Type':'application/json'}
def thread_function():
    time.sleep(2)
    while 1:
        r= requests.put(endpoints['auction'].get_prefix() + "update_auction_items_state",headers=headers)
        time.sleep(1)

item_state_updater_thread = threading.Thread(target=thread_function)
item_state_updater_thread.start()

@app.route("/bid_item", methods=['PUT'])
def bid_item():
    item_key = int(request.json['item_key'])
    user_key = int(request.json['user_key'])
    bid_price = float(request.json['bid_price'])
    if items_db.contains(doc_id=item_key):
        item = itemsdb.get(doc_id=item_key)
        if item['auction_state'] != 'started':
            return jsonify(Acknowledgement_base(False,"item is not in bidding state").serialize())
        else:
            # valuate bids
            start_bidding_price = float(item['start_bidding_price'])
            buyout_price = float(item['buyout_price'])
            highest_bidding_price = float(item['highest_bidding_price'])
            if bid_price < start_bidding_price:
                return jsonify(Acknowledgement_base(False,"bid price < start bidding price").serialize())
            if bid_price <= highest_bidding_price:
                return jsonify(Acknowledgement_base(False,"bid price <= highest_bidding_price").serialize())

            #correct biding price if bid_price is higher than buyout price
            if bid_price >= buyout_price:
                bid_price = buyout_price
            #if reach here,valid bid, update winning_bidder_key, highest_bidding_price
            items_db.update({'winning_bidder_key':user_key, 'highest_bidding_price':bid_price}, doc_ids=[item_key])
            return jsonify(Acknowledgement_base(True).serialize())
    else:
        return jsonify(Acknowledgement_base(False,"item does not exist").serialize())

@app.route("/create_auction_item", methods=['PUT'])
def create_auction_item():
    key = items_db.insert({'name': request.json['name'], 'start_time':request.json['start_time'], 'end_time': request.json['end_time'], 'category': request.json['category'], 'start_bidding_price': request.json['start_bidding_price'], 'buyout_price': request.json['buyout_price'], 'user_key':int(request.json['user_key']), 'winning_bidder_key':-1, 'highest_bidding_price':-1, 'auction_state':'created'})
    items_db.update({'key':key}, doc_ids=[key])
    return jsonify(Item_Ack(True, key).serialize())

@app.route("/update_auction_item/<int:key>", methods=['PUT'])
def update_auction_item(key):
    if items_db.contains(doc_id=key):
        item = items_db.get(doc_id=key)
        if item['auction_state'] != 'created':
            return jsonify(Acknowledgement_base(False,"item has passed the state allowing modification").serialize())
        # find the item from db using key and update its properties
        items_db.update(request.json, doc_ids=[key])
        return jsonify(Item_Ack(True, key).serialize())
    return jsonify(Item_Ack(False, key).serialize())

# this is periodically(every second) called by state_updater service externally
@app.route("/update_auction_items_state", methods=['PUT'])
def update_auction_items_state():
    now = datetime.now()
    for item in items_db:
        start_time = datetime.strptime(item['start_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(item['end_time'], '%Y-%m-%d %H:%M:%S')
        #print (start_time)
        #print (end_time)
        #print (now)
        # hit buyout, auction close
        if item['highest_bidding_price'] >= item['buyout_price']:
            items_db.update({'auction_state':'closed'}, doc_ids=[item.doc_id])
            #TODO notify user_service ?
        # check auction window and determine state
        if item['auction_state'] == 'created' and now >= start_time:
            items_db.update({'auction_state':'started'}, doc_ids=[item.doc_id])
        if now>=end_time:
            items_db.update({'auction_state':'closed'}, doc_ids=[item.doc_id])
            #TODO notify user_service ?
    return jsonify({'refresh_timestamp':now.strftime("%Y-%m-%d %H:%M:%S")})

@app.route("/remove_auction_item/<int:key>", methods=['PUT'])
def remove_auction_item(key):
    # find the item from db using key and delete the record from db
    if items_db.contains(doc_id=key):
        item = items_db.get(doc_id=key)
        if item['auction_state'] != 'created':
            return jsonify(Acknowledgement_base(False,"item has passed the state allowing removal").serialize())
        items_db.remove(doc_ids=[key])
        return jsonify(Item_Ack(True, key).serialize())
    return jsonify(Item_Ack(False, key).serialize())

@app.route("/get_all_auction_items", methods=['GET'])
def get_all_auction_items():
    query = Query()
    ret = items_db.search(query.auction_state == 'started')
    return jsonify(ret)

@app.route("/get_auction_items_by_key/<int:item_key>", methods=['GET'])
def get_auction_items_by_key(item_key):
    query = Query()
    ret = items_db.search(query.key == item_key)
    return jsonify(ret)

@app.route("/get_auction_items_by_user/<int:user_key>", methods=['GET'])
def get_auction_items_by_user(user_key):
    print(user_key)
    query = Query()
    ret = items_db.search(query.user_key == user_key)
    print(ret)
    return jsonify(ret)

@app.route("/get_auction_items_by_keyword/<string:keyword>", methods=['GET'])
def get_auction_items_by_keyword(keyword):
    query = Query()
    regex = ".*" + keyword + ".*" #any string contains a substring of keyword
    matched = items_db.search(query.name.matches(regex, flags=re.IGNORECASE))
    ret = []
    for item in matched:
        if item['auction_state'] == 'started':
            ret.append(item)
    return jsonify(ret)

@app.route("/get_auction_items_by_category/<string:category>", methods=['GET'])
def get_auction_items_by_category(category):
    query = Query()
    ret = items_db.search( (query.category == category) & (query.auction_state == 'started') )
    return jsonify(ret)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6664, debug=True)
