import requests
import json
from class_types import Item_base, Endpoint
from tinydb import TinyDB, Query
import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("key")
args = parser.parse_args()

pp = pprint.PrettyPrinter(indent=4)
endpoints = {}
items_db = TinyDB('items.json')
with open("endpoints.json") as endpoints_config:
    data = json.load(endpoints_config)
    for idx,ep in enumerate(data['services']):
        endpoints[ep['domain']] = Endpoint(ep['domain'],ep['ip'],ep['port'])
#pp.pprint(endpoints)

headers = {'Content-Type':'application/json'}
dummy_item = {'name':'Zion Williamson', 'start_time':'2020-12-21 11:30:05', 'end_time':'2021-01-27 13:30:05', 'category':'nba_draft', 'start_bidding_price':777, 'buyout_price':12000, 'user_key':1}

r= requests.put(endpoints['mediator'].get_prefix() + "create_auction_item", data=json.dumps(dummy_item),headers=headers)
print(r.json(),r.status_code)

#dummy_item_update = {'name':'ben simmons', 'start_time':'2020-11-21 11:30:05', 'end_time':'2020-11-21 12:30:05', 'category':'nba_draft_2016', 'start_bidding_price':'6666666', 'buyout_price':'29000000', 'user_key':'0'}

#r=requests.put(endpoints['mediator'].get_prefix() + "update_auction_item/"+args.key, data=json.dumps(dummy_item_update), headers=headers)
#print(r.json())

#r=requests.get(endpoints['mediator'].get_prefix() + "get_auction_items_by_key/" + args.key, headers=headers)
#print(r.json())

#r=requests.get(endpoints['mediator'].get_prefix() + "get_all_auction_items", headers=headers)
#print(r.json())

#r=requests.put(endpoints['mediator'].get_prefix() + "remove_auction_item/"+args.key, headers=headers)
#print(r.json())

#r=requests.get(endpoints['mediator'].get_prefix() + "get_auction_items_by_category/nba_draft", headers=headers)
#print(r.json())

#r=requests.get(endpoints['mediator'].get_prefix() + "get_auction_items_by_keyword/kevin",headers=headers)
#print(r.json())

#r=requests.get(endpoints['mediator'].get_prefix() + "get_auction_items_by_user/1", headers=headers)
#print(r.json())
