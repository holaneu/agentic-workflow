from workflows import WORKFLOWS_REGISTRY
from assistants import ASSISTANTS_REGISTRY
from tools import *

# root_folder = os.path.dirname(os.path.abspath(__file__))
# os.chdir(root_folder) # Change the working directory to the directory containing this executed py file

# ----------------------
# playground:
# ----------------------

if __name__ == "__main__":
  # print('\nopenai:\n', fetch_ai("gpt-4o-mini", "What is the capital of France?"))

  # print('\nmistral:\n', fetch_ai("mistral-small-latest", "What is the capital of France?"))

  # print('\ngemini:\n', fetch_ai("gemini-1.5-flash", "What is the capital of France?"))

  # save_to_file(content=fetch_ai(input="what is the capital of Czechia? Write only the name and nothing else", model="mistral-small-latest"), filepath="test/test.txt")

  # print(fetch_ai(input="write ahoj", model="mistral-small-latest"))    

  # print(ASSISTANTS['assistant_translator_cs_en_yaml']['function'](input="namazat si chleba"))

  # WORKFLOWS_REGISTRY['workflow_translation_cs_en_yaml']['function'](input="interrogate", model="gemini-2.0-flash-exp")

  # print(fetch_ai(model="gemini-2.0-flash-exp", input="kedlubna"))

  # print(fetch_ai(model="gpt-4o-mini", input="kedlubna"))

  """
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
  """

  # print(call_api_newsapi(query="openai OR claude OR deepseek OR mistral", domains="techcrunch.com,thenextweb.com", lastDays=5))

  # print(generate_id(10))

  # print(current_datetime_iso())

  # print(brave_search("openai"))

  # print(download_web_sourcecode("https://martinvlach.cz/zivot-se-ma-zit-ne-vymyslet/"))
 
  # print(download_web_readable_content("https://martinvlach.cz/zivot-se-ma-zit-ne-vymyslet/", "body main h1, body main p, body main bloquete"))

  """
  base_url="https://martinvlach.cz"
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
"""

# docs/_posts/2025-02-03-workflows-ideas-2.md
# docs/_posts/2025-02-03-workflows-ideas.md
"""
result = commit_to_github(
    files=["docs/_posts/2025-02-03-workflows-ideas-2.md"],
    commit_message="Add new blog post",
    repo_name="holaneu/auto-posts",
    branch="dev"
)
"""

from private.urls_list import urls
base_url = os.getenv('MV_BASE_URL')
for url in urls[20:]:
  parsed_content = download_web_readable_content(url, "body main h1, body main p, body main bloquete")
  url_edited = url.replace(base_url, "").replace("/", "")
  save_to_file(content=parsed_content, filepath=output_folder_path("downloaded_articles/" + url_edited + ".txt"))
  print(f" *** saved: {url_edited}.txt")