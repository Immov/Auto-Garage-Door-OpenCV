import requests
r = requests.post('http://192.168.4.1:80/set_data', data="{'number':55}") // remember that you get the keyword 'number' in the server side
print(r.text) // should print "Some message"