import requests

session = requests.Session()


def handle_thing(ip: str, action: str, user: str, passw: str, body=None):
    try:
        endpoint = thing[action]['link']
    except Exception as e:
        print(e)
        return 'handle_thing:wrong action used.'
    url = ip+endpoint
    r = thing[action]['method'](url, u=user, p=passw, data=body)
    print(r)
    if hasattr(r, 'status_code'):
        if str(r.status_code) in thing[action]['response']:
            return 'HTTP Response:' + str(r.status_code) + ' ' + thing[action]['response'][str(r.status_code)]
        else:
            return 'HTTP Response:' + str(r.status_code) + ' ' + str(r.text)
    else:
        return r


def handle_item(ip: str, action: str, user: str, passw: str, body=None):
    try:
        endpoint = item[action]['link']
    except Exception as e:
        print(e)
        return 'handle_item:wrong action used.'
    url = ip + endpoint
    r = item[action]['method'](url, u=user, p=passw, data=body)
    print(r)
    if hasattr(r, 'status_code'):
        if str(r.status_code) in item[action]['response']:
            return 'HTTP Response:' + str(r.status_code) + ' ' + item[action]['response'][str(r.status_code)]
        else:
            return 'HTTP Response:' + str(r.status_code) + ' ' + str(r.text)
    else:
        return r


def handle_link(ip: str, action: str, user: str, passw: str, body=None):
    try:
        url_add = requests.utils.quote(body['itemName']+'/'+body['channelUID'])
        endpoint = links[action]['link']+'/'+url_add
    except Exception as e:
        print(e)
        return 'handle_link:wrong action used or keyerror in data'
    url = ip + endpoint
    r = links[action]['method'](url, u=user, p=passw, data=body)
    print(r)
    if hasattr(r, 'status_code'):
        if str(r.status_code) in links[action]['response']:
            return 'HTTP Response:' + str(r.status_code) + ' ' + links[action]['response'][str(r.status_code)]
        else:
            return 'HTTP Response:' + str(r.status_code) + ' ' + str(r.text)
    else:
        return r


def http_get(url, u, p, data=None):
    try:
        headers = {'Content-type': 'application/json'}
        session.auth = (u, p)
        r = session.get(url, json=data, headers=headers, verify=False, timeout=2)
        return r
    except requests.exceptions.Timeout as e:
        return 'Connection to '+ url +' timed out. Please verify the url and retry, please.'
    except requests.exceptions.TooManyRedirects as e:
        return 'Bad URL. Please verify the url and retry, please.'
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        return e


def http_post(url, u, p, data=None):
    try:
        headers = {'Content-type': 'application/json'}
        session.auth = (u, p)
        r = session.post(url, json=data, headers=headers, verify=False, timeout=2)
        return r
    except requests.exceptions.Timeout as e:
        return 'Connection to '+ url +' timed out. Please verify the url and retry, please.'
    except requests.exceptions.TooManyRedirects as e:
        return 'Bad URL. Please verify the url and retry, please.'
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        return e


def http_put(url, u, p, data=None):
    try:
        headers = {'Content-type': 'application/json'}
        session.auth = (u, p)
        r = session.put(url, json=data, headers=headers, verify=False, timeout=2)
        return r
    except requests.exceptions.Timeout as e:
        return 'Connection to '+ url +' timed out. Please verify the url and retry, please.'
    except requests.exceptions.TooManyRedirects as e:
        return 'Bad URL. Please verify the url and retry, please.'
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        return e


item =  {'list':{
                'link':'/rest/items?recursive=false',
                'type':http_get,
                'response':{
                    '200':'OK'}
                },
          'create':{
                'link': '/rest/items',
                'method': http_put,
                'response':{
                  '200': 'OK',
                  '400': 'Payload is invalid'}
                },
          'update':{
                'link':'/rest/items',
                'method':http_put,
                'response':{
                    '200':'OK',
                    '400':'Payload is invalid'}
                }
          }

thing =  {'list':{
                'link':'/rest/things',
                'method':http_get,
                'response':{
                    '200':'OK'}
                },
          'create':{
                'link':'/rest/things',
                'method':http_post,
                'response':{
                   '201':'Thing created',
                   '400':'A uid must be provided, if no binding can create a thing of this type',
                   '409':'A thing with the same uid already exists',
                   '500':'UID must have at least 3 segments'}
               },
          'update':{
                'link':'/rest/things/',
                'method':http_put,
                'response':{
                   '200':'OK',
                   '404':'Thing not found',
                   '409':'Thing could not be updated as it is not editable'}
                }
          }

links =  {'list':{
                'link':'/rest/links',
                'type':http_get,
                'response':{
                    '200':'OK'}
                },
          'create':{
                'link': '/rest/links',
                'method': http_put,
                'response':{
                  '200': 'OK',
                  '400': 'Content does not match the path',
                  '405': 'Link is not editable'}
                }
          }
