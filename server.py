from flask import Flask, request, render_template, jsonify
from app import workflow_translation_out_yaml, workflow_summarization

app = Flask(__name__)

# Define available workflows
WORKFLOWS = {
    'translate': {
        'name': 'Translation CS-EN',
        'function': workflow_translation_out_yaml,
        'model': 'gpt-4o-mini' #'gemini-1.5-flash'
    },
    'summarize': {
        'name': 'Text Summarization', 
        'function': workflow_summarization,
        'model': 'gpt-4o-mini'
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