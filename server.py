from flask import Flask, request, render_template, jsonify
from workflows import WORKFLOWS_REGISTRY
from assistants import ASSISTANTS_REGISTRY  # You'll need to create this
import inspect

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html', workflows=WORKFLOWS_REGISTRY, assistants=ASSISTANTS_REGISTRY)

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        process_type = data.get('type')
        
        if not process_type:
            return jsonify({'error': 'Missing process type'}), 400
            
        if process_type == 'workflow':
            workflow_id = data.get('workflow')
            if not workflow_id:
                return jsonify({'error': 'Missing workflow ID'}), 400
                
            workflow = WORKFLOWS_REGISTRY.get(workflow_id)
            if not workflow:
                return jsonify({'error': 'Invalid workflow'}), 400
            
            # Get function parameters
            func_params = inspect.signature(workflow['function']).parameters
            
            # Build kwargs based on required parameters
            kwargs = {}
            if 'input' in func_params:
                input_text = data.get('input')
                if input_text is None:
                    return jsonify({'error': 'Missing required input'}), 400
                kwargs['input'] = input_text
                
            if 'model' in func_params:
                kwargs['model'] = workflow['model']
                
            result = workflow['function'](**kwargs)
            
        elif process_type == 'assistant':
            # Similar logic for assistants
            assistant_id = data.get('assistant')
            if not assistant_id:
                return jsonify({'error': 'Missing assistant ID'}), 400
                
            assistant = ASSISTANTS_REGISTRY.get(assistant_id)
            if not assistant:
                return jsonify({'error': 'Invalid assistant'}), 400
                
            # Get function parameters
            func_params = inspect.signature(assistant['function']).parameters
            
            # Build kwargs based on required parameters
            kwargs = {}
            if 'input' in func_params:
                input_text = data.get('input')
                if input_text is None:
                    return jsonify({'error': 'Missing required input'}), 400
                kwargs['input'] = input_text
                
            if 'model' in func_params:
                kwargs['model'] = assistant['model']
                
            result = assistant['function'](**kwargs)
            
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
