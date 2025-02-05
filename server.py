from flask import Flask, request, render_template, jsonify
from workflows import WORKFLOWS
from assistants import ASSISTANTS  # You'll need to create this

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html', workflows=WORKFLOWS, assistants=ASSISTANTS)

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        input_text = data.get('input')
        process_type = data.get('type')
        
        if not input_text or not process_type:
            return jsonify({'error': 'Missing input or process type'}), 400
            
        if process_type == 'workflow':
            workflow_id = data.get('workflow')
            if not workflow_id:
                return jsonify({'error': 'Missing workflow ID'}), 400
                
            workflow = WORKFLOWS.get(workflow_id)
            if not workflow:
                return jsonify({'error': 'Invalid workflow'}), 400
                
            result = workflow['function'](
                input=input_text,
                model=workflow['model']
            )
            
        elif process_type == 'assistant':
            assistant_id = data.get('assistant')
            if not assistant_id:
                return jsonify({'error': 'Missing assistant ID'}), 400
                
            assistant = ASSISTANTS.get(assistant_id)
            if not assistant:
                return jsonify({'error': 'Invalid assistant'}), 400
                
            result = assistant['function'](
                input=input_text,
                model=assistant['model']
            )
            
        else:
            return jsonify({'error': 'Invalid process type'}), 400
        
        return jsonify({
            'success': True,
            'response': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
