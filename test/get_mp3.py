import requests
import hashlib
import time
import sys

def get_mp3_url(tsid):
    timestamp = str(int(time.time()))
    sign_str = f'TSID={tsid}&appid=16073360&timestamp={timestamp}0b50b02fd0d73a9c4c8c3a781c30845f'
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    
    url = 'https://music.91q.com/v1/song/tracklink'
    params = {
        'appid': '16073360',
        'timestamp': timestamp,
        'TSID': tsid,
        'sign': sign
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://music.91q.com'
    }
    
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if 'data' in data and 'path' in data['data']:
        print(data['data']['path'])
    else:
        print('无法获取下载地址')

if __name__ == '__main__':
    get_mp3_url('T10062807773') 