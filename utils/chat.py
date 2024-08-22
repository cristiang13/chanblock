import os
# import openai
from openai import OpenAI

client = OpenAI()
def getResponseChatGpt(input, coin):
 
  message_log = [
    {"role": "system", "content": f"Think step by step. Relax and breathe /n you are a expert in Blockchain and {coin} network.."},
    {"role": "user", "content": input}
  ]
  completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=600,         # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
        top_p=1,
        n=1,
        timeout=180,
        frequency_penalty=0,
        presence_penalty=0,  
    )
  response = completion.choices[0].message.content
  return response