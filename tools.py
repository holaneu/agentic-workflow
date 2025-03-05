import os
import requests
import json
import re
import datetime
from configs import *
from pathlib import Path


def tool(**kwargs):
  """Decorator to define tool functions with metadata."""
  def decorator(func):
      func.id = func.__name__  # Automatically set id to the function name
      func.name = kwargs.get('name', func.__name__.replace('', '').replace('_', ' '))  # Use function name as default name
      func.description = kwargs.get('description', func.__doc__)  # Use function docstring if no description
      func.category = kwargs.get('category', None)  # Assign None if category is not provided
      func.is_tool = True
      return func
  return decorator


@tool()
def get_model(model_name):
  """
  Retrieves an AI model configuration from a list of available models by its name.
  Args:
    model_name (str): The name of the AI model to search for.
  Returns:
    dict or None: The model configuration dictionary if found, None otherwise. 
    The model dictionary contains model parameters and settings.
  """
  for model in ai_models:
    if model['name'] == model_name:
      return model
  return None


@tool()
def format_input_as_messages(input):
    if isinstance(input, str):
        return [{"role": "user", "content": input}]
    return input


@tool()
def fetch_ai(model, input):
  """
  Fetches AI response using specified model and input.
  This function processes the input through different AI models based on their API type.
  Currently supports OpenAI and Anthropic API types.
  Args:
    model (str or dict): The AI model identifier or configuration dictionary
    input (str): The input text/prompt to be processed by the AI model
  Returns:
    str or None: The AI model's response if successful, None if the model is not found
    or if the API type is not supported
  Example:
    >>> response = fetch_ai("gpt-4", "What is the capital of France?")
    >>> print(response)
    "The capital of France is Paris."
  """
  model = get_model(model)
  if model is None:
    return None
  if model['api_type'] == 'openai':
    return call_api_of_type_openai_v2(model, input)
    #return call_api_of_type_openai_official(model, input)
  if model['api_type'] == 'anthropic':
    return call_api_of_type_anthropic(model, input)
  return None


@tool()
def call_api_of_type_openai_official(model, input):
  from openai import OpenAI
  client = OpenAI()
  try:
    completion = client.chat.completions.create(
      model=model['name'],
      messages=format_input_as_messages(input)
    )
    log_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filepath = f"logs/ai_response_{log_timestamp}.log"    
    # Convert completion object to dictionary for JSON serialization
    completion_dict = {
      "model": completion.model,
      "choices": [{
        "message": {
          "content": completion.choices[0].message.content,
          "role": completion.choices[0].message.role
        }
      }],
      "usage": {
        "prompt_tokens": completion.usage.prompt_tokens,
        "completion_tokens": completion.usage.completion_tokens,
        "total_tokens": completion.usage.total_tokens
      }
    }    
    log_content = {
      "input": format_input_as_messages(input),
      "output": completion_dict
    }
    log_content = json.dumps(log_content, ensure_ascii=False, indent=2)
    save_to_file(content=log_content, filepath=log_filepath)
    output = {
        "status": "call_api_of_type_openai_official: Success",
        "message": {
          "content": completion.choices[0].message.content,
          "role": completion.choices[0].message.role,
        },        
        "info": {
          "model": completion.model,
          "prompt_tokens": completion.usage.prompt_tokens,
          "completion_tokens": completion.usage.completion_tokens,
          "total_tokens": completion.usage.total_tokens
        }
      }
    return output
  except Exception as e:
    print(f"Error calling OpenAI: {e}")
    return None


@tool()
def call_api_of_type_openai_v2(model, input):
  """
  Calls OpenAI API v2 with the given model and input.
  This function sends a request to OpenAI's API, handles the response, logs the interaction,
  and returns the processed result.
  Args:
    model (dict): Dictionary containing model information including 'name'
    input (str/dict): Input text or formatted input to be sent to the API
  Returns:
    dict: A dictionary containing:
      - status (str): Status message
      - message (dict): 
        - content (str): The generated content
        - role (str): Role of the message
      - info (dict):
        - model (str): Model name used
        - prompt_tokens (int): Number of tokens in prompt
        - completion_tokens (int): Number of tokens in completion
        - total_tokens (int): Total tokens used
    None: If the API call fails or encounters an error
  Raises:
    Exception: If there's an error during the API call
  Note:
    - Requires valid model data with api_key and base_url
    - Logs all interactions in 'logs' directory with timestamp
    - Uses temperature of 0.7 for generation
  """
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
      log_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
      log_filepath = f"logs/ai_response_{log_timestamp}.log"
      log_content = {
        "input": format_input_as_messages(input),
        "output": result
      }
      log_content = json.dumps(log_content, ensure_ascii=False, indent=2)
      save_to_file(content=log_content, filepath=log_filepath)
      output = {
        "status": "call_api_of_type_openai_v2: Success",
        "message": {
          "content": result["choices"][0]["message"]["content"],
          "role": result["choices"][0]["message"]["role"]
        },        
        "info": {
          "model": result["model"],
          "prompt_tokens": result["usage"]["prompt_tokens"],
          "completion_tokens": result["usage"]["completion_tokens"],
          "total_tokens": result["usage"]["total_tokens"]
        }
      }
      #return result["choices"][0]["message"]["content"]
      return output
    else:
      print(f"Error: {response.status_code}")
      print(response.text)
      return None
  except Exception as e:
    print(f"Error calling model: {e}")
    return None


@tool()
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


@tool()
def call_api_newsapi(query=None, lastDays=None, domains=None):
  """
  Fetches news articles from NewsAPI based on configured settings.
  Returns:
    dict: News articles data or None if request fails
  """
  base_url = "https://newsapi.org/v2/everything"
  today = datetime.datetime.now()
  start_date = today - datetime.timedelta(days=lastDays)
  from_date = start_date.strftime("%Y-%m-%d")
  to_date = today.strftime("%Y-%m-%d")

  params = {
    "q": query,
    "searchIn": "title,description",
    "from": from_date,
    "to": to_date,
    "sortBy": "popularity",
    "language": "en",
    "domains": domains,
    "apiKey": os.getenv("NEWSAPI_API_KEY"),
    "pageSize": 20,
    "page": 1
  }

  try:
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
      return response.json()
    else:
      print(f"Error: {response.status_code}")
      print(response.text)
      return None
  except Exception as e:
    print(f"Error calling NewsAPI: {e}")
    return None


@tool()
def open_file(filepath):
  """
  Opens and reads a text file, returning its contents as a string.
  Args:
    filepath (str): The path to the file to be opened and read.
  Returns:
    str: The complete contents of the file as a string.
  Raises:
    FileNotFoundError: If the specified file does not exist.
    IOError: If there is an error reading the file.
  """
  with open(filepath, 'r', encoding='utf-8') as infile:
      return infile.read()


def save_to_file(filepath, content, prepend=False):
  """Saves content to a file with various safety checks and options.
  This function saves the provided content to a file, with options to prepend or append. 
  It includes several safety checks for content validity and file path security.
  Args:
    filepath (str): Relative path where the file should be saved. Path traversal is not allowed.
    content (str or convertible to str): Content to write to the file. Cannot be empty.
    prepend (bool, optional): If True, adds content at the beginning of file. If False, appends to end. 
      Defaults to False.
  Raises:
    ValueError: If content is empty, not convertible to string, contains invalid Unicode,
      exceeds 10MB, or if filepath attempts path traversal.
    IOError: If there are issues with file operations.
    OSError: If there are system-level errors during file operations.
  Notes:
    - Creates directories in the path if they don't exist
    - Adds newline after content
    - Files are written using UTF-8 encoding
    - Maximum file size limit is 10MB
    - Paths are relative to APP_SETTINGS["output_folder"]
  """
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


def save_to_external_file(filename, content, prepend=False, base_path=None):
    """Save content to a file in an external location, creating directories if needed."""
    # Use environment variable if set, otherwise use default path
    base_path = base_path or os.getenv('EXTERNAL_STORAGE_PATH', APP_SETTINGS['locale_dropbox_path'])
    base_path = Path(base_path)
    full_path = base_path / filename
    
    # Validate path is outside project directory
    try:
        if not full_path.is_absolute():
            full_path = full_path.resolve()
        if not str(full_path).startswith(str(base_path)):
            raise ValueError("Path must be within the external storage directory")
            
        # Create directories if they don't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        mode = 'r+' if full_path.exists() else 'w'
        if prepend and full_path.exists():
            existing_content = full_path.read_text(encoding='utf-8')
            full_path.write_text(content + existing_content, encoding='utf-8')
        else:
            write_mode = 'a' if full_path.exists() else 'w'
            with open(full_path, write_mode, encoding='utf-8') as f:
                f.write(content)
                
    except Exception as e:
        print(f"Error saving to external file: {e}")
        raise


@tool()
def save_to_json_file(data, output_file):
  """Saves data to a JSON file with UTF-8 encoding.
  Args:
    data: The data to be saved to the JSON file. Can be any JSON-serializable object.
    output_file (str): The path to the output JSON file.
  Example:
    data = {"name": "John", "age": 30}
    save_to_json_file(data, "output.json")
  """
  with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


@tool()
def split_and_strip(content):
  """
  Splits a string by a delimiter of 5 or more hyphens and strips whitespace from each part.
  Args:
    content (str): The input string to be split and stripped.
  Returns:
    list[str]: A list of strings where:
      - Each string is a part of the original content split by 5 or more hyphens
      - Leading and trailing whitespace is removed from each part
      - Empty strings are preserved
  Example:
    >>> text = "Hello\\n-----\\nWorld"
    >>> split_and_strip(text)
    ['Hello', 'World']
  """
  parts = re.split(r'-{5,}', content.strip())
  stripped_parts = [part.strip() for part in parts]
  return stripped_parts


@tool()
def generate_id(length=10):    
  """
  Generate a random ID string of specified length using letters and numbers.  
  Args:
    length (int): Length of ID to generate, defaults to 10    
  Returns:
    str: Random string of specified length containing letters and digits    
  Example:
    >>> generate_id()
    'bK9mP4xL2n'
    >>> generate_id(5)
    'Yw3kP'
  """
  import random
  import string
  chars = string.ascii_letters + string.digits
  return ''.join(random.choice(chars) for _ in range(length))


@tool()
def current_datetime_iso():
    """
    Returns the current datetime in ISO 8601 format.
    Returns:
        str: Current datetime in ISO 8601 format (e.g. "2025-03-05T11:00:29.307714+00:00")
    Example:
        >>> current_datetime_iso()
        '2025-03-05T11:00:29.307714+00:00'
    """
    return datetime.datetime.now(datetime.timezone.utc).isoformat()    


@tool(category='database')
def json_db_load(filepath: str) -> dict:
    """
    Load JSON database from a file.
    Args:
        filepath (str): Path to the JSON database file
    Returns:
        dict: Database content or empty dict if file not found
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


@tool(category='database')
def json_db_save(filepath: str, data: dict) -> None:
    """
    Save JSON database to a file.
    Args:
        filepath (str): Path to save the JSON database
        data (dict): Data to save
    """
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


@tool(category='database')
def json_db_add_entry(db_file_path: str, collection: str, entry: dict) -> str:
    """
    Add a new entry to a collection in the JSON database.
    Args:
        db_file_path (str): Database file path
        collection (str): Name of the collection
        entry (dict): Entry data to add
    Returns:
        str: ID of the added entry
    """
    db_data = json_db_load(db_file_path)
    if "collections" not in db_data:
        db_data["collections"] = {}        
    if collection not in db_data["collections"]:
        db_data["collections"][collection] = []        
    entry_id = entry.get("id", generate_id())
    entry["id"] = entry_id    
    db_data["collections"][collection].append(entry)    
    json_db_save(db_file_path, db_data)    
    return entry_id


@tool(category='database')
def json_db_get_entry(filepath: str, collection: str, entry_id: str) -> dict:
    """
    Retrieve a single entry by ID from the database.
    Args:
        filepath (str): Database file path
        collection (str): Collection name
        entry_id (str): Entry ID to find
    Returns:
        dict: Entry data or None if not found
    """
    db = json_db_load(filepath)
    return next((entry for entry in db.get(collection, []) 
                if entry["id"] == entry_id), None)


@tool(category='database')
def json_db_update_entry(filepath: str, collection: str, entry_id: str, updates: dict) -> bool:
    """
    Update an existing entry by ID.
    Args:
        filepath (str): Database file path
        collection (str): Collection name
        entry_id (str): Entry ID to update
        updates (dict): New data to update
    Returns:
        bool: True if updated successfully
    """
    db = json_db_load(filepath)
    for entry in db.get(collection, []):
        if entry["id"] == entry_id:
            entry.update(updates)
            json_db_save(filepath, db)
            return True
    return False


@tool(category='database')
def json_db_delete_entry(filepath: str, collection: str, entry_id: str) -> bool:
    """
    Delete an entry by ID from the database.
    Args:
        filepath (str): Database file path
        collection (str): Collection name
        entry_id (str): Entry ID to delete
    Returns:
        bool: True if deleted successfully
    """
    db = json_db_load(filepath)
    original_len = len(db.get(collection, []))
    db[collection] = [e for e in db.get(collection, []) if e["id"] != entry_id]
    if len(db[collection]) < original_len:
        json_db_save(filepath, db)
        return True
    return False


# Extract all tools dynamically
import inspect
TOOLS_REGISTRY = {
    func.id: {
      'name': func.name, 
      'description': func.description, 
      'function': func, 
      'category': func.category
    }
    for name, func in inspect.getmembers(__import__(__name__), inspect.isfunction)
    if hasattr(func, 'id') and hasattr(func, 'is_tool')  # Check for workflow marker
}
