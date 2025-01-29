from flask import Flask, request, render_template, jsonify
from app import workflow_translation_out_yaml, workflow_summarization, workflow_situation_analysis, workflow_video_transcription_summarization, workflow_explain_simply_lexicon

app = Flask(__name__, static_folder='static', template_folder='templates')

# Define available workflows
WORKFLOWS = {
    'translate': {
        'name': 'Translation CS-EN (YAML)',
        'function': workflow_translation_out_yaml,
        'model': 'gpt-4o-mini' #'gemini-1.5-flash'
    },
    'summarize': {
        'name': 'Text Summarization', 
        'function': workflow_summarization,
        'model': 'gpt-4o-mini'
    },
    'analyze_situation': {
        'name': 'Analyze situation', 
        'function': workflow_situation_analysis,
        'model': 'gpt-4o'
    },
    'summarize_video_transcription': {
        'name': 'summarize_video_transcription', 
        'function': workflow_video_transcription_summarization,
        'model': 'gpt-4o'
    },
    'explain_simply_lexicon': {
      'name': 'explain_simply_lexicon', 
      'function': workflow_explain_simply_lexicon,
      'model': 'gpt-4o'
    }
}

@app.route('/')
def index():
    return render_template('index.html', workflows=WORKFLOWS)

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        input_text = data.get('input')
        workflow_id = data.get('workflow')
        
        if not input_text or not workflow_id:
            return jsonify({'error': 'Missing input or workflow'}), 400
            
        workflow = WORKFLOWS.get(workflow_id)
        if not workflow:
            return jsonify({'error': 'Invalid workflow'}), 400
            
        # Execute the selected workflow
        result = workflow['function'](
            input=input_text,
            model=workflow['model']
        )
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)