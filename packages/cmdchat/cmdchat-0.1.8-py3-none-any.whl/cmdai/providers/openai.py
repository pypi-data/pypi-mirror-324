import openai
from openai import OpenAI
from ..config import get_api_key

def get_response(query, model):
    api_key = get_api_key('openai')
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        store=True,
        messages=[{"role": "user", "content": query}]
    )
    return completion.choices[0].message['content'].strip()
