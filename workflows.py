from assistants import *
from tools import save_to_file

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


@workflow(name='Translation CS-EN (YAML)')
def workflow_translation_out_yaml(input, model=None):
    """Translates text between Czech and English in YAML format."""
    if input is None:
        return None 
    translation = assistant_translator_cs_en_yaml(input=input, model=model)
    if translation:
        #translation = translation.strip()
        translation = translation["message"]["content"].strip()
        save_to_file("test/slovnicek.txt", translation + "\n\n-----\n", prepend=True)
    return translation


@workflow()
def workflow_text_summarization(input, model=None):
    """Summarizes input text."""
    if input is None:
        return None 
    summarization = assistant_summarize_text(input=input, model=model)
    if summarization:
        summarization = summarization["message"]["content"].strip()
        save_to_file("test/summaries.txt", summarization + "\n\n-----\n", prepend=True)
    return summarization


@workflow()
def workflow_situation_analysis(input, model=None):
    """Analyzes a given situation and provides insights."""
    if input is None:
        return None 
    analysis = assistant_analyze_situation(input=input, model=model)
    if analysis:
        analysis = analysis["message"]["content"].strip()
        save_to_file("test/situace.txt", analysis + "\n\n-----\n", prepend=True)
    return analysis


@workflow()
def workflow_video_transcript_summarization(input, model=None):
    """Summarizes the transcript of a video."""
    if input is None:
        return None 
    summarization = assistant_summarize_video_transcript(input=input, model=model)
    if summarization:
        summarization = summarization["message"]["content"].strip()
        save_to_file("test/video_transcript_summaries.txt", summarization + "\n\n-----\n", prepend=True)
    return summarization


@workflow()
def workflow_explain_simply_lexicon(input, model=None):
    """Provides simple explanations, synonyms, and examples for a given phrase."""
    if input is None:
        return None 
    lexicon = assistant_explain_simply_lexicon(input=input, model=model)
    if lexicon:
        lexicon = lexicon["message"]["content"].strip()
        save_to_file("test/lexicon.txt", lexicon + "\n\n-----\n", prepend=True)
    return lexicon


# Extract all workflows dynamically
import inspect
WORKFLOWS = {
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
