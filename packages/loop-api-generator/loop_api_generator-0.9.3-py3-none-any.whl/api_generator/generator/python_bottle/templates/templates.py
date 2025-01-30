INITIALIZE_TEMPLATE = """
from bottle import Bottle, run

app = Bottle()
"""

GET_TEMPLATE = """
{{ anchor_get_main_begin }}
@app.get('/{{ route }}')
def get_{{ route_name }}():
    return {"message": "GET {{ route }} called"}{{ new_get_route }}
"""

POST_TEMPLATE = """
{{ anchor_post_main_begin }}
@app.post('/{{ route }}')
def post_{{ route_name }}():
    return {"message": "POST {{ route }} called"}{{ new_post_route }}
"""

PUT_TEMPLATE = """
{{ anchor_put_main_begin }}
@app.put('/{{ route }}')
def put_{{ route_name }}():
    return {"message": "PUT {{ route }} called"}{{ new_put_route }}
"""

PATCH_TEMPLATE = """
{{ anchor_patch_main_begin }}
@app.patch('/{{ route }}')
def patch_{{ route_name }}():
    return {"message": "PATCH {{ route }} called"}{{ new_patch_route }}
"""

DELETE_TEMPLATE = """
{{ anchor_delete_main_begin }}
@app.delete('/{{ route }}')
def delete_{{ route_name }}():
    return {"message": "DELETE {{ route }} called"}{{ new_delete_route }}
"""

FINALIZE_TEMPLATE = """
{{ anchor_delete_route_begin }}
if __name__ == "__main__":
    run(app, host='{{ host }}', port={{ port }}, debug=True)
{{ anchor_finalize_end }}
"""
