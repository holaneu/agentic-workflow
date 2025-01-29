from workflows import WORKFLOWS
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

  print(fetch_ai(input="write ahoj", model="mistral-small-latest"))  

  #print(WORKFLOWS['translation_out_yaml']['function']("houska", "gpt-4o-mini"))

