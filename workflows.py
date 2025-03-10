from assistants import *
from tools import save_to_file, save_to_external_file, call_api_newsapi, json_db_add_entry, current_datetime_iso, generate_id, output_folder_path, open_file
from configs import APP_SETTINGS
import json
import os

def workflow(**kwargs):
    """Decorator to define workflow functions with metadata."""
    def decorator(func):
        func.id = func.__name__  # Automatically set id to the function name
        func.name = kwargs.get('name', func.__name__.replace('workflow_', '').replace('_', ' '))  # Use function name as default name
        func.description = kwargs.get('description', func.__doc__)  # Use function docstring if no description
        func.model = kwargs.get('model', None)  # Assign None if model is not provided
        func.category = kwargs.get('category', None)  # Assign None if category is not provided
        func.is_workflow = True
        return func
    return decorator


@workflow()
def workflow_translation_cs_en_yaml(input, model=None):
    """Translates text between Czech and English in YAML format."""
    if input is None or input.strip() == "":
        return "No input provided." 
    translation = assistant_translator_cs_en_yaml(input=input, model=model)
    if translation:
        translation = translation["message"]["content"].strip()
        save_to_file(output_folder_path("slovnicek.txt"), translation + "\n\n-----\n", prepend=True)
    return translation


@workflow()
def workflow_translation_cs_en(input, model=None):
    """Translates text between Czech and English."""
    if input is None:
        return None 
    translation = assistant_translator_cs_en(input=input, model=model)
    if translation:
        translation = translation["message"]["content"].strip()
        save_to_file(output_folder_path("translations.txt"), translation + "\n\n-----\n", prepend=True)
    return translation


@workflow()
def workflow_text_summarization(input, model=None):
    """Summarizes input text."""
    if input is None:
        return None 
    summarization = assistant_summarize_text(input=input, model=model)
    if summarization:
        summarization = summarization["message"]["content"].strip()
        save_to_file(output_folder_path("summaries.txt"), summarization + "\n\n-----\n", prepend=True)
    return summarization


@workflow()
def workflow_situation_analysis(input, model=None):
    """Analyzes a given situation and provides insights."""
    if input is None:
        return None 
    analysis = assistant_analyze_situation(input=input, model=model)
    if analysis:
        analysis = analysis["message"]["content"].strip()
        save_to_file(output_folder_path("situace.txt"), analysis + "\n\n-----\n", prepend=True)
    return analysis


@workflow()
def workflow_video_transcript_summarization(input, model=None):
    """Summarizes the transcript of a video."""
    if input is None:
        return None 
    summarization = assistant_summarize_video_transcript(input=input, model=model)
    if summarization:
        summarization = summarization["message"]["content"].strip()
        save_to_file(output_folder_path("video_transcript_summaries.txt"), summarization + "\n\n-----\n", prepend=True)
    return summarization


@workflow()
def workflow_explain_simply_lexicon(input, model=None):
    """Provides simple explanations, synonyms, and examples for a given phrase."""
    if input is None:
        return None 
    lexicon = assistant_explain_simply_lexicon(input=input, model=model)
    if lexicon:
        lexicon = lexicon["message"]["content"].strip()
        save_to_file(output_folder_path("lexicon.txt"), lexicon + "\n\n-----\n", prepend=True)
    return lexicon


@workflow()
def workflow_create_assistatnt_prompt(input, model=None):
    """Creates a new assistant based on the input."""
    if input is None:
        return None 
    assistant = assistant_assistant_instructions_creator(input=input, model=model)
    if assistant:
        assistant = assistant["message"]["content"].strip()
        save_to_file(output_folder_path("assistants.txt"), assistant + "\n\n-----\n", prepend=True)
    return assistant


@workflow()
def workflow_take_quick_note(input, model=None):
    """Takes a quick note and saves it to both JSON database and file."""
    if input is None:
        return None 
    note = input.strip()
    db_entry = {
        "id": generate_id(10),
        "created_at": current_datetime_iso(),
        "updated_at": current_datetime_iso(),
        "content": note
    }
    db_file_path = output_folder_path("databases/quick_notes.json") 
    json_db_add_entry(db_file_path=db_file_path, collection="notes", entry=db_entry)
    save_to_file(output_folder_path("quick_notes.md"), note + "\n\n-----\n", prepend=True)
    #save_to_external_file("quick_notes_2025_H1_test.md", input.strip() + "\n\n-----\n", prepend=True)    
    return note


@workflow()
def workflow_write_story(input, model=None):
    """Generates short feel-good stories."""
    if input is None:
        return None 
    story = assistant_writer(input=input, model=model)
    if story:
        story = story["message"]["content"].strip()
        save_to_file(output_folder_path("stories.md"), story + "\n\n-----\n", prepend=True)
    return story


@workflow()
def workflow_download_ai_news():
    """Downloads and saves recent AI-related news articles."""
    news = call_api_newsapi(query="openai OR mistral OR claude", lastDays=5, domains="techcrunch.com,thenextweb.com")
    if news:
        formatted_news = json.dumps(news, indent=2)
        save_to_file(output_folder_path("news.md"), formatted_news + "\n\n-----\n", prepend=True)
        return formatted_news
    return "no output"


@workflow()
def workflow_quiz_from_text(input, model=None):	
    """
    Processes a text input and generates quiz questions with answers in json format.    
    """
    if input is None:   
      return "no input provided"
    source_text = input.strip()
    instructions_questions = f"""Na základě zdrojového textu napiš otázky, které se ptají na podstatné informace uvedené ve zdrojovém textu. Přidej ke každé otázce také stručnou odpověď. Pravidla: 
    Na každou otázku bude vždy pouze jedna jednoznačná správná odpověď. 
    Používej samostatné otázky tzn. rozděl složené otázky na jednotlivé samostatné otázky, aby nebylo nutné odpovídat na více věcí najednou.

    <output_format>
    - [otázka 1] ([odpověď na otázku 1])
    - [otázka 2] ([odpověď na otázku 2])
    - [otázka 3] ([odpověď na otázku 3])
    ...
    </output_format>

    <example>
    Zdroj: Nejdelší řeka ČR je Vltava. Nejvýznamnější přítoky řeky Vltavy jsou Berounka a Sázava. Vltava se vlévá do řeky Labe ve městě Mělník.

    Otázky:
    - Jaké je nejdelší řeka v ČR? (Vltava)
    - Jaké jsou nejvýznamnější přítoky Vltavy? (Berounka a Sázava)
    - Do jaké řeky se vlévá Vltava? (Labe)
    - Ve kterém městě se nachází soutok Vltavy a Labe? (Mělník)
    </example>

    Zdrojový text:
    {source_text}
  """

    questions = assistant_universal_no_instructions(input=instructions_questions, model="gpt-4o")
    if not questions or not questions.get("message", {}).get("content"):
        return "no questions generated"
    questions = questions.get("message", {}).get("content", "").strip()
    save_to_file(output_folder_path("questions.txt"), questions + "\n\n-----\n", prepend=True)  
    instructions_quiz_questions = f"""
    Zdrojový text:
    {source_text}

    Otázky:
    {questions}

    Otázky byly vygenerovány na základě zdrojového textu. Pokud je některá otázka nejasná nebo chybná, uprav ji tak, aby byla správná a jednoznačná. 
    Dále ke každé otázce přidej dvě další možnosti odpovědí, které budou nesprávné.

    Výstup vypiš dle šablony výstupu a nepřidávej žádné další texty, fráze, nebo komentáře.
    
    Šablona výstupu:
    {{
      "id": {generate_id(6)},
      "name": "<quiz title>",
      "created": {current_datetime_iso()},
      "tags": ["<topic in one word>"],
      "questions": [
        {{
          "question": "<question 1 title>",
          "options": ["<option 1>", "<option 2>", "<option 3>"],
          "answer": <index of one option from options array representing correct answer>
        }},
        {{
          "question": "<question X title>",
          "options": ["<option 1>", "<option 2>", "<option 3>"],
          "answer": <index of one option from options array representing correct answer>
        }}
      ]
    }}
    """
    quiz_questions = assistant_universal_no_instructions(input=instructions_quiz_questions, model="gpt-4o")
    if not quiz_questions:
        return "no quiz questions generated"
    quiz_questions = quiz_questions.get("message", {}).get("content", "").strip()
    save_to_file(output_folder_path("quizzes.txt"), quiz_questions + "\n\n-----\n", prepend=True)
    return quiz_questions
    

@workflow()
def workflow_exctract_theses(input, model=None):
    """Exctracts all theses from the input text and saves output to the persistant memory."""
    if input is None:
        return "No input provided." 
    source_text = input.strip()
    instructions_theses = f"""Analyzuj zdrojový text a extrahuj všechny tvrzení (teze) ze zdrojového textu a vypiš je ve strukturovaných bodech. Teze jsou krátké výroky, které shrnují hlavní myšlenku nebo obsah textu. Zajisti úplnost extrakce bez vynechání jakékoli teze. Zachovej původní význam, důležité informace a přesnost formulací. Nepřidávej žádné komentáře ani fráze, ani na začátek, ani na konec tvé odpovědi.

    Vstupní text:
    {source_text}

    Výstup:
    - [teze 1]
    - [teze 2]
    - [teze 3]
    """
    theses = assistant_universal_no_instructions(input=instructions_theses, model="gpt-4o")
    if not theses or not theses.get("message", {}).get("content"):
        return "no tezis generated"
    theses = theses.get("message", {}).get("content", "").strip()
    save_to_file(output_folder_path("theses.txt"), theses + "\n\n-----\n", prepend=True) 
    return theses



# Extract all workflows dynamically
import inspect
WORKFLOWS_REGISTRY = {
    func.id: {
      'name': func.name, 
      'description': func.description, 
      'function': func, 
      'model': func.model, 
      'category': func.category
    }
    for name, func in inspect.getmembers(__import__(__name__), inspect.isfunction)
    if hasattr(func, 'id') and hasattr(func, 'is_workflow')  # Check for workflow marker
}
