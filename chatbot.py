import os
from openai import OpenAI

API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)

def query(user_question,prompt):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system","content":prompt},
            {"role":"user","content":user_question},
        ],
        temperature=0.5
    )
    return response.choices[0].message.content
