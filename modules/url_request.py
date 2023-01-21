from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
req = Request("http://192.168.1.8/mjpeg/1")
try:
    response = urlopen(req)
except HTTPError as e:
    # do something
    print('Error code: ', e.code)
except URLError as e:
    # do something
    print('Reason: ', e.reason)
else:
    # do something
    print('good!')
    print("Result code:" + str(response.getcode()))
