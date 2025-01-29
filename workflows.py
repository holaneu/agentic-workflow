# workflows.py

def workflow(id, name, description):
    """Decorator to define workflow functions with metadata."""
    def decorator(func):
        func.id = id
        func.name = name
        func.description = description
        return func
    return decorator

@workflow(id='translation_out_yaml', name='Translation CS-EN (YAML)', description='Translates text between Czech and English in YAML format')
def workflow_translation_out_yaml(input, model):
    from app import assistant_translator_cs_en_yaml, save_to_file
    if input is None:
        return None 
    translation = assistant_translator_cs_en_yaml(input=input, assistant_model=model)
    if translation:
        translation = translation.strip()
        save_to_file("test/slovnicek.txt", translation + "\n\n-----\n", prepend=True)
    return translation

@workflow(id='summarize', name='Text Summarization', description='Summarizes input text')
def workflow_summarization(input, model):
    from app import assistant_summarize_text, save_to_file
    if input is None:
        return None 
    summarization = assistant_summarize_text(input=input, model=model)
    if summarization:
        summarization = summarization.strip()
        save_to_file("test/summaries.txt", summarization + "\n\n-----\n", prepend=True)
    return summarization

@workflow(id='analyze_situation', name='Analyze situation', description='Analyzes a given situation and provides insights')
def workflow_situation_analysis(input, model):
    from app import assistant_analyze_situation, save_to_file
    if input is None:
        return None 
    analysis = assistant_analyze_situation(input=input, model=model)
    if analysis:
        analysis = analysis.strip()
        save_to_file("test/situace.txt", analysis + "\n\n-----\n", prepend=True)
    return analysis

@workflow(id='summarize_video_transcription', name='Summarize Video Transcription', description='Summarizes the transcript of a video')
def workflow_video_transcription_summarization(input, model):
    from app import assistant_summarize_video_transcription, save_to_file
    if input is None:
        return None 
    summarization = assistant_summarize_video_transcription(input=input, model=model)
    if summarization:
        summarization = summarization.strip()
        save_to_file("test/video_transcript_summaries.txt", summarization + "\n\n-----\n", prepend=True)
    return summarization

@workflow(id='explain_simply_lexicon', name='Explain Simply (Lexicon)', description='Provides simple explanations, synonyms, and examples')
def workflow_explain_simply_lexicon(input, model):
    from app import assistant_explain_simply_lexicon, save_to_file
    if input is None:
        return None 
    lexicon = assistant_explain_simply_lexicon(input=input, model=model)
    if lexicon:
        lexicon = lexicon.strip()
        save_to_file("test/lexicon.txt", lexicon + "\n\n-----\n", prepend=True)
    return lexicon

# Extract all workflows dynamically
import inspect
WORKFLOWS = {
    func.id: {'name': func.name, 'description': func.description, 'function': func, 'model': 'gpt-4o'}
    for name, func in inspect.getmembers(__import__(__name__), inspect.isfunction)
    if hasattr(func, 'id')
}
