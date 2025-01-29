from flask import Flask, request, render_template, jsonify
from workflows import WORKFLOWS

app = Flask(__name__, static_folder='static', template_folder='templates')

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
            
        # Execute the selected workflow and get response
        result = workflow['function'](
            input=input_text,
            model=workflow['model']
        )
        
        # Return the workflow result
        return jsonify({
            'success': True,
            'response': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
