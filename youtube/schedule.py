import requests
import time

while 1:
    resp = requests.get("http://youtube_web:5000/videos/auto")
    time.sleep(10)
