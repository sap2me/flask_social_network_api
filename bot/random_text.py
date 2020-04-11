import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.getatext.online',
    'Connection': 'keep-alive',
    'Referer': 'https://www.getatext.online/',
    'TE': 'Trailers',
}


def get_random_text(language='english', paragraphs=1):
    data_string = '{"upper":false,"html":false,"language":"'+language+'","howMany":"'+str(paragraphs)+'"}'
    data = {
      'type': 'generate',
      'data': data_string
    }
    try:
        response = requests.post('https://www.getatext.online/comm/server.ashx', 
                                 headers=headers,
                                 data=data,
                                 timeout=(7, 10))
        response.raise_for_status()
        json_data = response.json()
        return json_data['texts'][0]

    except Exception as e:
        print(f'Error: {e}')

