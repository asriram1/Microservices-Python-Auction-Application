from admin_DB import *
from admin_API import *

import requests
APIBaseURL = 'http://172.17.0.2:3308'

endpointdict = {
        'login': f'{APIBaseURL}/admin/login',
        'sign_up': f'{APIBaseURL}/admin/sign_up',
        'logout': f'{APIBaseURL}/admin/logout',
        'changeusername': f'{APIBaseURL}/admin/username_change'
    }


def admin_signup(username, password):
    try:
        # this is the one that can access the endpoint dictionary directly
        resp = requests.post(endpointdict['sign_up'],
                                json={'username': username, 'password': password})

    except KeyError:
        # register endpoint isn't defined in the endpoint dictionary
        return False
    except requests.exceptions.ConnectionError:
        # API is down
        return False
    except requests.exceptions.InvalidURL:
        # URL is invalid in the endpoint dictionary
        return False
    # 200 is the only valid response here,
    # all others indicate that the user could not be registered
    return resp.status_code == 200


def admin_login(username, password):
    try:
        # this is the one that can access the endpoint dictionary directly
        resp = requests.post(endpointdict['login'],
                                json={'username': username, 'password': password})

    except KeyError:
        # register endpoint isn't defined in the endpoint dictionary
        return False
    except requests.exceptions.ConnectionError:
        # API is down
        return False
    except requests.exceptions.InvalidURL:
        # URL is invalid in the endpoint dictionary
        return False
    # 200 is the only valid response here,
    # all others indicate that the user could not be registered
    return resp.status_code == 200


def admin_logout(username):
    try:
        # this is the one that can access the endpoint dictionary directly
        resp = requests.post(endpointdict['logout'],
                                json={'username': username})

    except KeyError:
        # register endpoint isn't defined in the endpoint dictionary
        return False
    except requests.exceptions.ConnectionError:
        # API is down
        return False
    except requests.exceptions.InvalidURL:
        # URL is invalid in the endpoint dictionary
        return False
    # 200 is the only valid response here,
    # all others indicate that the user could not be registered
    return resp.status_code == 200

def admin_changeusername(new_username, old_username):
    try:
        # this is the one that can access the endpoint dictionary directly
        resp = requests.post(endpointdict['changeusername'],
                                json={'old_username': old_username, 'new_username': new_username})

    except KeyError:
        # register endpoint isn't defined in the endpoint dictionary
        return False
    except requests.exceptions.ConnectionError:
        # API is down
        return False
    except requests.exceptions.InvalidURL:
        # URL is invalid in the endpoint dictionary
        return False
    # 200 is the only valid response here,
    # all others indicate that the user could not be registered
    return resp.status_code == 200


def main():
    admin_signup('admin_user', 'pass')
    #admin_login('admin_user', 'pass')
    #admin_logout('admin_user', 'pass')
    # admin_changeusername('new_admin_2', 'admin_user')
    


if __name__ == "__main__":
    main()

