import os
import requests
import json
import re
import datetime
from configs import *


def get_model(model_name):
  for model in ai_models:
    if model['name'] == model_name:
      return model
  return None


def format_input_as_messages(input):
    if isinstance(input, str):
        return [{"role": "user", "content": input}]
    return input


def fetch_ai(model, input):
  model = get_model(model)
  if model is None:
    return None
  if model['api_type'] == 'openai':
    return call_api_of_type_openai_v2(model, input)
  if model['api_type'] == 'gemini':
    return call_api_of_type_gemini_v1(model, input)
  if model['api_type'] == 'anthropic':
    return call_api_of_type_anthropic(model, input)
  return None


def call_api_of_type_openai_official(model, input):
  from openai import OpenAI
  client = OpenAI()
  try:
    completion = client.chat.completions.create(
      model=model['name'],
      messages=format_input_as_messages(input)
    )
    return completion.choices[0].message.content
  except Exception as e:
    print(f"Error calling OpenAI: {e}")
    return None


def call_api_of_type_openai_v2(model, input):
  model_data = get_model(model['name'])
  if model_data is None:
    print("no model data")
    return None
  
  headers = {
    "Authorization": f"Bearer {model_data['api_key']}",
    "Content-Type": "application/json"
  }

  payload = {
    "model": model_data['name'],
    "messages": format_input_as_messages(input),
    "temperature": 0.7
  }

  try:
    response = requests.post(model_data['base_url'], headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
      result = response.json()
      print(result)
      log_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
      log_filepath = f"logs/ai_response_{log_timestamp}.log"
      log_content = json.dumps(result, ensure_ascii=False, indent=2)
      save_to_file(content=log_content, filepath=log_filepath)
      return result["choices"][0]["message"]["content"]
    else:
      print(f"Error: {response.status_code}")
      print(response.text)
      return None
  except Exception as e:
    print(f"Error calling model: {e}")
    return None


def call_api_of_type_gemini_v1(model, input):
  model_data = get_model(model['name'])
  if model_data is None:
    print("no model data")
    return None

  messages = format_input_as_messages(input)
  # Concatenate content from all messages
  prompt_text = "\n".join([msg['content'] for msg in messages])
  
  base_url = f"{model_data['base_url']}/{model_data['name']}:generateContent"
  
  headers = {
    "Content-Type": "application/json"
  }

  payload = {
    "contents": [{
      "parts": [{"text": prompt_text}]
    }]
  }

  params = {
    "key": model_data['api_key']
  }

  try:
    response = requests.post(base_url, headers=headers, params=params, data=json.dumps(payload))
    if response.status_code == 200:
      result = response.json()
      return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
      print(f"Error: {response.status_code}")
      print(response.text)
      return None
  except Exception as e:
    print(f"Error calling model: {e}")
    return None


def call_api_of_type_anthropic(model, messages):
  model_data = get_model(model['name'])
  if model_data is None:
    print("no model data")
    return None

  messages = format_input_as_messages(messages)
  
  headers = {
    "x-api-key": model_data['api_key'],
    "anthropic-version": "2023-06-01",
    "Content-Type": "application/json"
  }

  payload = {
    "model": model_data['name'],
    "messages": messages,
    "max_tokens": 1024
  }

  try:
    response = requests.post(model_data['base_url'], headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
      result = response.json()
      return result["content"][0]["text"]
    else:
      print(f"Error: {response.status_code}")
      print(response.text)
      return None
  except Exception as e:
    print(f"Error calling model: {e}")
    return None


def open_file(filepath):
  with open(filepath, 'r', encoding='utf-8') as infile:
      return infile.read()


def save_to_file(filepath, content, prepend=False):
  try:
    if content is None:
      raise ValueError("Content cannot be empty")
    if not isinstance(content, str):
      content = str(content)
      if not isinstance(content, str):
        raise ValueError("Content must be a convertible to string")
    if len(content.strip()) == 0:
      raise ValueError("Content cannot be empty")
    if ".." in filepath or filepath.startswith("/"):
      raise ValueError("Invalid filepath: Path traversal not allowed")    
    
    full_path = os.path.join(APP_SETTINGS["output_folder"], filepath)
    directory = os.path.dirname(full_path)
    if directory and not os.path.exists(directory):
      os.makedirs(directory)
    
    try:
      content_size = len(content.encode('utf-8'))
    except UnicodeEncodeError:
      raise ValueError("Content contains invalid Unicode characters")
    if content_size > 10 * 1024 * 1024:
      raise ValueError("Content too large: Exceeds 10MB limit")
    
    if prepend:
      # Read existing content if file exists
      existing_content = ''
      if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as infile:
          existing_content = infile.read()
      # Write new content followed by existing content
      with open(full_path, 'w', encoding='utf-8') as outfile:
        outfile.write(content + '\n' + existing_content)
    else:
      # Normal append mode
      with open(full_path, 'a', encoding='utf-8') as outfile:
        outfile.write(content + '\n')
        
  except (IOError, OSError) as e:
    print(f"Error writing to file {filepath}: {e}")
    raise
  except Exception as e:
    print(f"Unexpected error while saving file {filepath}: {e}")
    raise


def save_to_json_file(data, output_file):
  with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


def split_and_strip(content):
  parts = re.split(r'-{5,}', content.strip())
  stripped_parts = [part.strip() for part in parts]
  return stripped_parts