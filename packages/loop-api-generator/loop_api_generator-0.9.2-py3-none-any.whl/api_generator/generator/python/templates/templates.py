INITIALIZE_TEMPLATE = """
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, response_body):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_body).encode("utf-8"))
"""

GET_TEMPLATE = """
    {{ anchor_get_main_begin }}def do_GET(self):
        path = self.path.strip("/")
        try:
            if path == "{{ route }}":
                self._send_response(200, {"message": "GET {{ route }} called"}){{ new_get_route }}
            else:
                self._send_response(404, {"message": "Not found"})
            self._send_response(200, {"message": "GET method called"})
        except Exception as e:
            self._send_response(500, {"message": str(e)}){{ anchor_get_main_end }}
"""

GET_ROUTE_TEMPLATE = """
            {{ anchor_get_route_begin }}elif path == "/{{ route }}":
                self._send_response(200, {"message": "GET {{ route }} called"}){{ anchor_get_route_end }}{{ new_get_route }}"""

POST_TEMPLATE = """
    {{ anchor_post_main_begin }}def do_POST(self):
        path = self.path.strip("/")
        try:
            if path == "{{ route }}":
                self._send_response(200, {"message": "POST {{ route }} called"}){{ new_post_route }}
            else:
                self._send_response(404, {"message": "Not found"})
            self._send_response(200, {"message": "POST method called"})
        except Exception as e:
            self._send_response(500, {"message": str(e)}){{ anchor_post_main_end }}
"""

POST_ROUTE_TEMPLATE = """
            {{ anchor_post_route_begin }}elif path == "/{{ route }}":
                self._send_response(200, {"message": "POST {{ route }} called"}){{ anchor_post_route_end }}{{ new_post_route }}"""


PUT_TEMPLATE = """
    {{ anchor_put_main_begin }}def do_PUT(self):
        path = self.path.strip("/")
        try:
            if path == "{{ route }}":
                self._send_response(200, {"message": "PUT {{ route }} called"}){{ new_put_route }}
            else:
                self._send_response(404, {"message": "Not found"})
            self._send_response(200, {"message": "PUT method called"})
        except Exception as e:
            self._send_response(500, {"message": str(e)}){{ anchor_put_main_end }}
"""

PUT_ROUTE_TEMPLATE = """
            {{ anchor_put_route_begin }}elif path == "/{{ route }}":
                self._send_response(200, {"message": "PUT {{ route }} called"}){{ anchor_put_route_end }}{{ new_put_route }}"""

PATCH_TEMPLATE = """
    {{ anchor_patch_main_begin }}def do_PATCH(self):
        path = self.path.strip("/")
        try:
            if path == "{{ route }}":
                self._send_response(200, {"message": "PATCH {{ route }} called"}){{ new_patch_route }}
            else:
                self._send_response(404, {"message": "Not found"})
            self._send_response(200, {"message": "PATCH method called"})
        except Exception as e:
            self._send_response(500, {"message": str(e)}){{ anchor_patch_main_end }}
"""

PATCH_ROUTE_TEMPLATE = """
            {{ anchor_patch_route_begin }}elif path == "/{{ route }}":
                self._send_response(200, {"message": "PATCH {{ route }} called"}){{ anchor_patch_route_end }}{{ new_patch_route }}"""


DELETE_TEMPLATE = """
    {{ anchor_delete_main_begin }}def do_DELETE(self):
        path = self.path.strip("/")
        try:
            if path == "{{ route }}":
                self._send_response(200, {"message": "DELETE {{ route }} called"}){{ new_delete_route }}
            else:
                self._send_response(404, {"message": "Not found"})
            self._send_response(200, {"message": "DELETE method called"})
        except Exception as e:
            self._send_response(500, {"message": str(e)}){{ anchor_delete_main_end }}
"""

DELETE_ROUTE_TEMPLATE = """
            {{ anchor_delete_route_begin }}elif path == "/{{ route }}":
                self._send_response(200, {"message": "DELETE {{ route }} called"}){{ anchor_delete_route_end }}{{ new_delete_route }}"""


FINALIZE_TEMPLATE = """
{{ anchor_delete_route_begin }}if __name__ == "__main__":
    server = HTTPServer(("{{ host }}", {{ port }}), RequestHandler)
    print("Starting server at http://{{ host }}:{{ port }}")
    server.serve_forever(){{ anchor_finalize_end }}"""
