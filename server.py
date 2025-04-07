from flask import Flask, request, render_template, jsonify, abort
from workflows import WORKFLOWS_REGISTRY
from assistants import ASSISTANTS_REGISTRY  # You'll need to create this
import inspect
from storage.manager import FileStorageManager
import os
from configs import APP_SETTINGS

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuration
FILES_FOLDER = APP_SETTINGS['output_folder']
file_manager = FileStorageManager(FILES_FOLDER)

@app.template_filter('active_page')
def active_page(current_page, page_name):
    return 'active' if current_page == page_name else ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/workflows')
def workflows():
    return render_template('workflows.html', workflows=WORKFLOWS_REGISTRY, assistants=ASSISTANTS_REGISTRY)


@app.route('/files')
@app.route('/files/folder/<item_id>')
def files(item_id=None):
    structure = file_manager.get_structure()
    items_list = structure['items']
    
    # Get current folder and build breadcrumb path
    current_folder = None
    breadcrumbs = []
    
    if item_id:
        current_folder = next((item for item in items_list if item.id == item_id), None)
        if not current_folder or current_folder.type != 'folder':
            abort(404)
            
        # Build breadcrumbs
        temp_folder = current_folder
        while hasattr(temp_folder, 'parent'):
            parent = next((item for item in items_list if item.id == temp_folder.parent), None)
            if parent:
                breadcrumbs.insert(0, parent)
                temp_folder = parent
            else:
                break
        breadcrumbs.append(current_folder)
    
    # Filter items for current folder
    filtered_items = [
        item for item in items_list 
        if (not item_id and not hasattr(item, 'parent')) or
           (hasattr(item, 'parent') and item.parent == item_id)
    ]
    
    return render_template('files.html', 
                         items=filtered_items, 
                         current_folder=current_folder,
                         breadcrumbs=breadcrumbs)

@app.route('/files/file/<item_id>')
def item_detail(item_id):
    structure = file_manager.get_structure()
    item = next((item for item in structure['items'] if item.id == item_id), None)
    
    if not item or item.type != 'file':
        abort(404)
    
    # Generate breadcrumbs by traversing up through parent folders
    breadcrumbs = []
    if not hasattr(item, 'parent'):
        # If item has no parent, it's in the root folder
        breadcrumbs = [{'id': None, 'name': 'root', 'type': 'folder'}]
    else:
        current = next((i for i in structure['items'] if i.id == item.parent), None)
        while current:
            breadcrumbs.insert(0, current)
            current = next((i for i in structure['items'] if i.id == current.parent), None) if hasattr(current, 'parent') else None

    try:
        full_path = os.path.join(FILES_FOLDER, item.file_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template('file_detail.html', item=item, content=content, breadcrumbs=breadcrumbs)
    except Exception as e:
        abort(500)

@app.route('/database')
def database():
    return render_template('database.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/apps')
def apps():
    return render_template('apps.html')

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
    os.makedirs(FILES_FOLDER, exist_ok=True)
    app.run(debug=True, port=5000)
