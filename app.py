from dotenv import load_dotenv
import os
#from openai import OpenAI
import requests
import json
load_dotenv()

models = [
  {
    "name": "gpt-4o-mini",
    "base_url": "https://api.openai.com/v1/chat/completions",
    "api_key": os.getenv('OPENAI_API_KEY'),
    "provider": "openai"
  },
  {
    "name": "mistral-small-latest",
    "base_url": "https://api.mistral.ai/v1/chat/completions",
    "api_key": os.getenv('MISTRAL_API_KEY'),
    "provider": "mistral"
  }
]

def get_model(model_name):
  for model in models:
    if model['name'] == model_name:
      return model
  return None

def call_ai(model_name, prompt):
  model = get_model(model_name)
  if model is None:
    return None
  if model['provider'] == 'openai':
    return call_openai_v2(model, prompt)
  if model['provider'] == 'mistral':
    return call_openai_v2(model, prompt)
  return None

def call_openai_v2(model, prompt):
  model_data = get_model(model['name'])
  if model_data is None:
    print("no model data")
    return None

  print(model_data)

  headers = {
    "Authorization": f"Bearer {model_data['api_key']}",
    "Content-Type": "application/json"
  }

  payload = {
    "model": model_data['name'],
    "messages": [
      {"role": "user", "content": prompt}
    ],
    "temperature": 0.7
  }

  try:
    response = requests.post(model_data['base_url'], headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
      result = response.json()
      return result["choices"][0]["message"]["content"]
    else:
      print(f"Error: {response.status_code}")
      print(response.text)
      return None
  except Exception as e:
    print(f"Error calling model: {e}")
    return None


# ----------------------

print(call_ai("mistral-small-latest", "Hello, world!"))