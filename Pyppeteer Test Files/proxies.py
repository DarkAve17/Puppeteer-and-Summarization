import requests

proxies = {
    '',
    ''
}

response = requests.get('http://google.com', proxies=proxies)