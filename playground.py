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
    save_to_file(content=parsed_content, filepath=output_folder_path("downloaded_articles/" + url_edited + ".txt"))
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
    save_to_file(content=parsed_content, filepath=output_folder_path("downloaded_articles/" + url_edited + ".txt"))
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
  print('\n gpt-4o-mini:\n', fetch_ai("gpt-4o-mini", message1 + " " + message2, response_format=True))
  print('\n mistral-small-latest:\n', fetch_ai("mistral-small-latest", message1 + " " + message2, response_format=True))
  print('\n gemini-2.0-flash-lite:\n', fetch_ai("gemini-2.0-flash-lite", message1 + " " + message2, response_format=True))


def testing20250328():
  print("ocr openai:")
  print(extract_text_from_image_openai(file_path="private/ocr_test/tarotonline_02.png"))
  #print("ocr mistral:")
  #print(extract_text_from_image_mistral_ocr(file_path="private/ocr_test/tarotonline_02.png"))


# ------- run tests -------

if __name__ == "__main__": 
  # testing20250328()
  testing20250326_3()
  