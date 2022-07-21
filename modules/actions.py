import requests

def toggle_hexalight():
    url = "http://192.168.178.101:8123/api/webhook/wled-wz"
    x = requests.post(url)
    print("Hexalight toggle")

