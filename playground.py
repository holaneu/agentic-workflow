from workflows import WORKFLOWS_REGISTRY
from assistants import ASSISTANTS_REGISTRY
from tools import *

# root_folder = os.path.dirname(os.path.abspath(__file__))
# os.chdir(root_folder) # Change the working directory to the directory containing this executed py file

# ----------------------
# playground:
# ----------------------   

def testing1():
  print('\nopenai:\n', fetch_ai("gpt-4o-mini", "What is the capital of France?"))
  print('\nmistral:\n', fetch_ai("mistral-small-latest", "What is the capital of France?"))
  print('\ngemini:\n', fetch_ai("gemini-2.0-flash", "What is the capital of France?"))


def testing2():
  save_to_file(content=fetch_ai(input="what is the capital of Czechia? Write only the name and nothing else", model="mistral-small-latest"), filepath="test/test.txt")
  print(ASSISTANTS_REGISTRY['assistant_translator_cs_en_yaml']['function'](input="namazat si chleba"))
  WORKFLOWS_REGISTRY['workflow_translation_cs_en_yaml']['function'](input="interrogate", model="gemini-2.0-flash-exp")


def testing_registries():
  print("ASSISTANTS_REGISTRY")
  print(ASSISTANTS_REGISTRY)

  print("WORKFLOWS_REGISTRY")
  print(WORKFLOWS_REGISTRY)

  print("TOOLS_REGISTRY")
  tools_without_functions = {
    name: {k: v for k, v in tool.items() if k != 'function'}
    for name, tool in TOOLS_REGISTRY.items()
  }
  print(json.dumps(tools_without_functions, indent=2))


def testing20250317():
  base_url=os.getenv('MV_BASE_URL')
  urls = crawl_website_for_urls(
    start_url=f"{base_url}/rubrika/all/",
    url_pattern=f"{base_url}/rubrika/all/",
    max_pages=1000
  )
  print(f"\n *** urls: \n {urls} \n\n")
  specific_urls = extract_urls_from_pages(
      urls=urls,
      css_selector="body main"
  )
  print(f" *** specific_urls: \n {specific_urls} \n\n")
  for url in specific_urls[5:10]:
    parsed_content = download_web_readable_content(url, "body main h1, body main p, body main bloquete")
    url_edited = url.replace(base_url, "").replace("/", "")
    save_to_file(content=parsed_content, filepath=user_files_folder_path("downloaded_articles/" + url_edited + ".txt"))
    print(f" *** saved: {url_edited}.txt \n")
  print(" *** DONE *** \n\n")


def testing_github():
  # docs/_posts/2025-02-03-workflows-ideas-2.md
  # docs/_posts/2025-02-03-workflows-ideas.md  
  result = commit_to_github(
      files=["docs/_posts/2025-02-03-workflows-ideas-2.md"],
      commit_message="Add new blog post",
      repo_name="holaneu/auto-posts",
      branch="dev"
  )
  print(result)


def testing20250319():
  from private.urls_list import urls
  base_url = os.getenv('MV_BASE_URL')
  for url in urls[20:]:
    parsed_content = download_web_readable_content(url, "body main h1, body main p, body main bloquete")
    url_edited = url.replace(base_url, "").replace("/", "")
    save_to_file(content=parsed_content, filepath=user_files_folder_path("downloaded_articles/" + url_edited + ".txt"))
    print(f" *** saved: {url_edited}.txt")


def testing20250321():
  dbfile = "outputs/test/databases/quick_notes.json"
  print(json_db_get_entry(db_filepath=dbfile, collection="notes", entry_id="SQ99Ts3BNT"))
  print(json_db_update_entry(db_filepath=dbfile, collection="notes", entry_id="SQ99Ts3BNT", updates={"content": "mazlicek"}))
  # print(json_db_add_entry(db_filepath=dbfile, collection="notes", entry={"content": "prdolka 1"}))
  print(json_db_delete_entry(db_filepath=dbfile, collection="notes", entry_id="0bx7MHfAU0"))


def testing20250326_1():
  message="Write hello in uppercase format."
  print('\n gpt-4o-mini:\n', fetch_ai("gpt-4o-mini", message))
  print('\n gpt-4o:\n', fetch_ai("gpt-4o", message))
  print('\n mistral-small-latest:\n', fetch_ai("mistral-small-latest", message))
  print('\n mistral-large-latest:\n', fetch_ai("mistral-small-latest", message))
  print('\n gemini-2.0-flash:\n', fetch_ai("gemini-2.0-flash", message))
  print('\n gemini-2.0-flash-lite:\n', fetch_ai("gemini-2.0-flash", message))
  print('\n deepseek-chat:\n', fetch_ai("deepseek-chat", message))


def testing20250326_2():
  print(generate_id(10))
  print(current_datetime_iso())
  print(brave_search("openai"))
  print(download_news_newsapi(query="openai OR claude OR deepseek OR mistral", domains="techcrunch.com,thenextweb.com", lastDays=5))


def testing20250326_3():
  source = download_web_readable_content("https://www.menicka.cz/4550-bufacek-na-ruzku.html", "#menicka .content .text")
  jidla = ASSISTANTS_REGISTRY['assistant_universal_no_instructions']['function'](input=f"""{source} Jaka jidla jsou dnes v nabidce?""", model="gpt-4o-mini")
  

def testing20250326_4():
  message1="Alice and Bob are going to a science fair on Friday."
  message2="Extract the event information in json format."
  print('\n gpt-4o-mini:\n', fetch_ai("gpt-4o-mini", message1 + " " + message2, structured_output=True))
  print('\n mistral-small-latest:\n', fetch_ai("mistral-small-latest", message1 + " " + message2, structured_output=True))
  print('\n gemini-2.0-flash-lite:\n', fetch_ai("gemini-2.0-flash-lite", message1 + " " + message2, structured_output=True))


def testing20250328():
  print("ocr openai:")
  print(extract_text_from_image_openai(file_path="private/ocr_test/tarotonline_02.png"))
  #print("ocr mistral:")
  #print(extract_text_from_image_mistral_ocr(file_path="private/ocr_test/tarotonline_02.png"))


def testing20250408():
  tools_without_functions = {
    name: {k: v for k, v in tool.items() if k != 'function'}
    for name, tool in TOOLS_REGISTRY.items()
  }
  def decide_tool_for_task(task):
    instructions = f"""You are manager deciding which tools to use for a specific task.
    Available tools are: 
    {tools_without_functions}
    Your task is to choose the most suitable tool for the task: {task}.
    Use json format for output and include the following fields: tool, reason.
    """
    ai_response = fetch_ai("gemini-2.0-flash", instructions, structured_output=True)
    return ai_response
  
  task1 = "Extract the event information from the text. Use json format for output and include the following fields: event, date, time, location."
  task2 = "Translate the text from Czech to English."
  task3 = "Generate a summary of the text."
  task4 = "Generate id."  
  print(decide_tool_for_task(task3))
  print(decide_tool_for_task(task4))


def testing20250409():
  # step 1: search for restaurants in the area
  query = "obedove menu v blizkem okoli dluhonska 43 v prerove"
  search_results = brave_search(query=query, count=5)
  print(json.dumps(search_results, indent=2), end="\n\n")
  instructions = f"""Your task is to choose the most suitable search result for the origin query: {query}.
    Use json format for output and include the following fields: title, url.
    Search results: 
    {search_results}    
    """
  # step 2: choose the most suitable search result
  selected_search_result = fetch_ai(model="gemini-2.0-flash", input=instructions, structured_output=True)
  print(json.dumps(selected_search_result, indent=2), end="\n\n")
  if not selected_search_result['success']:
    return "somthing went wrong"  
  try:
    # step 3: parse the selected search result
    parsed_result = json.loads(selected_search_result.get('message', {}).get('content', ''))
    print(f"Parsed result: {parsed_result}", end="\n\n")
    if parsed_result and len(parsed_result) > 0:
      url = parsed_result[0].get('url', '')
      print(f"Selected URL: {url}", end="\n\n")
      if url:
        # step 4: download the content of the selected search result
        source = download_web_readable_content(url, "#menicka .content .text")
        print(source, end="\n\n")
    else:
      print("No valid URL found in search results")
  except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
  # step 5: extract foods and their origin restaurants from the text
  source_shorten = source[:len(source) // 4]
  source_shorten = source_shorten[100:]
  instructions2 = f"""Your task is to extract foods and its origin restaurants from a text.
    Use json format for output and include the following fields: food, restaurant.
    Text: {source_shorten}
    """
  extracted_foods = fetch_ai(model="gemini-2.0-flash", input=instructions2, structured_output=True)
  print(f"extracted foods: {json.dumps(extracted_foods.get('message', {}).get('content', ''), indent=2)}", end="\n\n")
  # step 6: clean the extracted foods data and print results
  try:
    import re
    cleaned_text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', extracted_foods.get('message', {}).get('content', ''))
    json_data = json.loads(cleaned_text)    
    print("extracted foods result:")
    print(json.dumps(json_data, indent=2, ensure_ascii=False), end="\n\n")
  except json.JSONDecodeError as e:
      print(f"Error parsing JSON: {e}")
      # Optional: Print the problematic part of the string
      error_position = e.pos
      context = cleaned_text[max(0, error_position-50):min(len(cleaned_text), error_position+50)]
      print(f"\nContext around error (pos {error_position}):")
      print(context)


def testing20250416():
  """Testing new model gpt-4.1. for deciding which tool to use for a specific task."""
  tools_without_functions = {
    name: {k: v for k, v in tool.items() if k != 'function'}
    for name, tool in TOOLS_REGISTRY.items()
  }
  def decide_tool_for_task(task):
    instructions = f"""You are manager deciding which tools to use for a specific task.
    Available tools are: 
    {tools_without_functions}
    Your task is to choose the most suitable tool for the task: {task}.
    Use json format for output and include the following fields: tool, reason.
    """
    ai_response = fetch_ai(model="gpt-4.1", input=instructions, structured_output=True)
    return ai_response
  
  task1 = "Extract the event information from the text. Use json format for output and include the following fields: event, date, time, location."
  task2 = "Translate the text from Czech to English."
  task3 = "Generate a summary of the text."
  task4 = "Generate id."  
  print('gpt-4.1 test', 'task3', decide_tool_for_task(task3), sep="\n", end="\n\n")
  print('gpt-4.1 test', 'task4', decide_tool_for_task(task4), sep="\n", end="\n\n")


def testing20250416_2():
  db_path=user_files_folder_path("databases/test1.json")
  # create new db without schema
  new_db = json_db_create_db_without_schema(db_filepath=db_path)
  print(f"db: {new_db}", end="\n\n")
  # add new entry to the db
  entry_content = {
    "content": f"test test {current_datetime_iso()}"
  }
  db_entry = json_db_add_entry(db_filepath=db_path, collection="entries", entry=entry_content)
  print(f"db_entry: {db_entry}", end="\n\n")
  # receive entry_id of the newly added entry
  if db_entry.get('success', False):
    db_entry_id = db_entry["data"]["entry_id"]
    print(f"db_entry_id: {db_entry_id}", end="\n\n")
  # load the whole db
  db = json_db_load(db_filepath=db_path)
  print(f"db: {db}", end="\n\n")  
  # get first collection
  db_collection_key = next(iter(db.get('collections', {}).keys()), None)
  print(f"db_collection_name: {db_collection_key}", end="\n\n")
  #db_collection = next(iter(db.get('collections', {}).values()), {})
  db_collection_value = db.get('collections', {}).get(db_collection_key, [])
  print(f"db_collection: {db_collection_value}", end="\n\n")
  # delete the last entry from the db
  last_entry_id = db_collection_value[-1].get('id', None)
  print(f"last_entry_id: {last_entry_id}", end="\n\n")
  removed_entry = json_db_delete_entry(db_filepath=db_path, collection=db_collection_key, entry_id=last_entry_id)
  print(f"removed_entry: {removed_entry}", end="\n\n")
  # update the first entry
  first_entry_id = db_collection_value[0].get('id', None)
  first_entry_content = db_collection_value[0].get('content', None)
  updated_entry_content = first_entry_content + " UPDATED"
  print(f"first_entry_id: {first_entry_id}", f"first_entry_content: {first_entry_content}", sep="\n", end="\n\n")
  updated_entry = json_db_update_entry(db_filepath=db_path, collection=db_collection_key, entry_id=first_entry_id, updates={"content": updated_entry_content})
  print(f"updated_entry: {updated_entry}", end="\n\n")



# ------- run tests -------

if __name__ == "__main__": 
  testing20250416_2()
  