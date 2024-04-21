"""
Imports for implementation
"""
from flask import request, jsonify
from app import webserver

@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """
    Handle POST request to /api/post_endpoint
    """
    if request.method == 'POST':
        data = request.json

        response = {"message": "Received data successfully", "data": data}

        return jsonify(response)

    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    Handle GET request to /api/get_results/<job_id>
    """
    job_counter = webserver.job_counter

    # Result is None when putting it in job_queue
    result = webserver.tasks_runner.job_id_dict.get(int(job_id))

    if job_counter <= int(job_id) or int(job_id) < 0:
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'})

    if result is None:
        return jsonify({'status': 'running'})

    return jsonify({'status': 'done', 'data': result})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    Handle POST request to /api/states_mean
    """
    data = request.json
    job_counter = webserver.job_counter
    webserver.tasks_runner.add_task(job_counter, data, '/api/states_mean', None, None)
    webserver.job_counter = job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    Handle POST request to /api/state_mean
    """
    data = request.json
    state = data['state']
    job_counter = webserver.job_counter
    webserver.tasks_runner.add_task(webserver.job_counter, data, '/api/state_mean', None, state)
    webserver.job_counter = job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    Handle POST request to /api/best5
    """
    data = request.json
    webserver.tasks_runner.add_task(webserver.job_counter, data, '/api/best5', None, None)
    webserver.job_counter = webserver.job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    Handle POST request to /api/worst5
    """
    data = request.json

    webserver.tasks_runner.add_task(webserver.job_counter, data, '/api/worst5', None, None)
    webserver.job_counter = webserver.job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    Handle POST request to /api/global_mean
    """
    data = request.json
    webserver.tasks_runner.add_task(webserver.job_counter, data, '/api/global_mean', None, None)
    webserver.job_counter = webserver.job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    Handle POST request to /api/diff_from_mean
    """
    data = request.json
    webserver.tasks_runner.add_task(webserver.job_counter, data, '/api/diff_from_mean', None, None)
    webserver.job_counter = webserver.job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    Handle POST request to /api/state_diff_from_mean
    """
    data = request.json
    state = data['state']
    webserver.tasks_runner.add_task(
    webserver.job_counter, data, '/api/state_diff_from_mean', None, state)
    webserver.job_counter = webserver.job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    Handle POST request to /api/mean_by_category
    """
    data = request.json
    webserver.tasks_runner.add_task(
    webserver.job_counter, data, '/api/mean_by_category', None, None)
    webserver.job_counter = webserver.job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    Handle POST request to /api/state_mean_by_category
    """
    data = request.json
    state = data['state']
    webserver.tasks_runner.add_task(
    webserver.job_counter, data, '/api/state_mean_by_category', None, state)
    webserver.job_counter = webserver.job_counter + 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/')
@webserver.route('/index')
def index():
    """
    Handle requests to the root and /index endpoints
    """
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"
    paragraphs = "\n".join([f"<p>{route}</p>" for route in routes])
    msg += paragraphs
    return msg

def get_defined_routes():
    """
    Get the defined routes in the webserver
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
