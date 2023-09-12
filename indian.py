import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import base64, json
from flask import Flask, request


app = Flask(__name__)

@app.route('/indian')
def indian():
    path = request.args.get('url')
    requests.utils.default_user_agent = lambda: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

    session = requests.Session()
    # session.proxies = {}
    # session.proxies['http'] = 'socks5h://localhost:9150'
    # session.proxies['https'] = 'socks5h://localhost:9150'
    # session.mount('https://', HTTPAdapter(max_retries=3))

    def decode(value):
        value_len = len(value)
        encoded_value = value[0:10] + value[value_len - 1] + value[12:value_len - 1]
        decoded_value = base64.b64decode(encoded_value).decode('utf-8')
        return json.loads(decoded_value)
    #https://einthusan.tv/movie/watch/4gpM/?lang=tamil
    r = session.get(url=path)
    page = BeautifulSoup(r.text, "html.parser")


    movie_page_url = path

    page_id = page.find('html')['data-pageid']
    ejpingables = page.find('section', {'id': 'UIVideoPlayer'})['data-ejpingables']

    movie_meta_url = movie_page_url.replace('movie', 'ajax/movie')

    payload = {
        'xEvent': 'UIVideoPlayer.PingOutcome',
        'xJson': '{\"EJOutcomes\":\"' + ejpingables + '\",\"NativeHLS\":false}',
        'gorilla.csrf.Token': page_id
    }

    encoded_url = session.post(movie_meta_url, data=payload).json()['Data']['EJLinks']

    print(decode(encoded_url)['MP4Link'])
    return decode(encoded_url)['MP4Link']

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
