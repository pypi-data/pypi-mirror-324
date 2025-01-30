INITIALIZE_TEMPLATE = """
from flask import Flask, jsonify

app = Flask(__name__)
"""

GET_TEMPLATE = """
{{ anchor_get_main_begin }}
@app.route('/{{ route }}', methods=['GET'])
def get_{{ route_name }}():
    return jsonify({"message": "GET {{ route }} called"}){{ new_get_route }}
"""

POST_TEMPLATE = """
{{ anchor_post_main_begin }}
@app.route('/{{ route }}', methods=['POST'])
def post_{{ route_name }}():
    return jsonify({"message": "POST {{ route }} called"}){{ new_post_route }}
"""

PUT_TEMPLATE = """
{{ anchor_put_main_begin }}
@app.route('/{{ route }}', methods=['PUT'])
def put_{{ route_name }}():
    return jsonify({"message": "PUT {{ route }} called"}){{ new_put_route }}
"""

PATCH_TEMPLATE = """
{{ anchor_patch_main_begin }}
@app.route('/{{ route }}', methods=['PATCH'])
def patch_{{ route_name }}():
    return jsonify({"message": "PATCH {{ route }} called"}){{ new_patch_route }}
"""

DELETE_TEMPLATE = """
{{ anchor_delete_main_begin }}
@app.route('/{{ route }}', methods=['DELETE'])
def delete_{{ route_name }}():
    return jsonify({"message": "DELETE {{ route }} called"}){{ new_delete_route }}
"""

FINALIZE_TEMPLATE = """
{{ anchor_finalize_begin }}
if __name__ == "__main__":
    app.run(host="{{ host }}", port={{ port }})
"""
