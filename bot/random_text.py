from tools import headers

import requests


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

