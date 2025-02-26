from workflows import WORKFLOWS_REGISTRY
from assistants import ASSISTANTS_REGISTRY
from tools import *

# root_folder = os.path.dirname(os.path.abspath(__file__))
# os.chdir(root_folder) # Change the working directory to the directory containing this executed py file


# ----------------------
# playground:
# ----------------------

if __name__ == "__main__":
  #print('\nopenai:\n', fetch_ai("gpt-4o-mini", "What is the capital of France?"))

  #print('\nmistral:\n', fetch_ai("mistral-small-latest", "What is the capital of France?"))

  #print('\ngemini:\n', fetch_ai("gemini-1.5-flash", "What is the capital of France?"))

  #save_to_file(content=fetch_ai(input="what is the capital of Czechia? Write only the name and nothing else", model="mistral-small-latest"), filepath="test/test.txt")

  #print(fetch_ai(input="write ahoj", model="mistral-small-latest"))    

  #print(ASSISTANTS['assistant_translator_cs_en_yaml']['function'](input="namazat si chleba"))

  WORKFLOWS_REGISTRY['workflow_translation_cs_en_yaml']['function'](input="interrogate", model="gemini-2.0-flash-exp")

  #print(fetch_ai(model="gemini-2.0-flash-exp", input="kedlubna"))

  #print(fetch_ai(model="gpt-4o-mini", input="kedlubna"))

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

  #print(call_api_newsapi(query="openai OR claude OR deepseek OR mistral", domains="techcrunch.com,thenextweb.com", lastDays=5))