class User_Base(object):
    def __init__(self, email):
        self.email_ = email

    def serialize(self):
        return {
            'email': self.email_,
        }

class User(User_Base):
    def __init__(self, email, password, login, suspend, items):
        self.email_ = email
        self.password_ = password
        self.login_ = False
        self.suspend_ = False
        self.items_ = []

    def serialize(self):
        return {
            'email': self.email_,
            'password': self.password_,
            'login': self.login_,
            'suspend': self.suspend_
        }

class Item_base(object):
    def __init__(self, key, name):
        self.key_ = key
        self.name_ = name
    def serialize(self):
        return{
            'key': self.key_,
            'name': self.name_,
    }

class Item_Auction(Item_base):
    def __init__(self, key):
        self.key_ = key
        # adding proproties for item of auction domain
        self.start_time_ = None
        self.end_time_ = None
        self.category_ = None
        self.bidding_info_ = None
        self.seller = None # base User object
        self.winning_bidder_ = None #base User object
        self.auction_state_ = None

class Bidding_Info(object):
    def __init__(self):
        self.start_bidding_price_ = None
        self.highest_bidding_price_ = None
        self.buyout_price_ = None


class Acknowledgement_base(object):
    def __init__(self, success, reason=""):
        self.success_ = success
        self.reason_ = reason
    def serialize(self):
        return{
            'success':self.success_,
            'reason':self.reason_
        }

class Item_Ack(Acknowledgement_base):
    def __init__(self, success, item_key):
        self.item_key_ = item_key
        self.success_ = success
    def serialize(self):
        return{
            'success':self.success_,
            'item_key':self.item_key_,
        }

class User_Ack(Acknowledgement_base):
    def __init__(self, success, user_key):
        self.user_key_ = user_key
        self.success_ = success
    def serialize(self):
        return{
            'success':self.success_,
            'user_key':self.user_key_,
        }

class Endpoint(object):
    def __init__(self, domain, ip, port):
        self.domain_ = domain
        self.ip_ = ip
        self.port_ = port

    def get_prefix(self):
        return self.ip_+":"+str(self.port_)+"/" # e.g. http://127.0.0.1:5000/