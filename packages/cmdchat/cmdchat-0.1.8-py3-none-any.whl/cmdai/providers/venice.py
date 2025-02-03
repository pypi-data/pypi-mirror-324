import requests
from ..config import get_api_key

def get_response(query, model):
    api_key = get_api_key('venice')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': query}]
    }
    response = requests.post('https://api.venice.ai/v1/chat/completions', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"Venice API request failed with status code {response.status_code}: {response.text}")
