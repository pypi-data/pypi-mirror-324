from io import BytesIO

from src.api_generator.generator.base_generator import BaseGenerator
from src.api_generator.generator.generator import Generator
from src.api_generator.generator.python_flask.templates import (
    DELETE_TEMPLATE,
    FINALIZE_TEMPLATE,
    GET_TEMPLATE,
    INITIALIZE_TEMPLATE,
    PATCH_TEMPLATE,
    POST_TEMPLATE,
    PUT_TEMPLATE,
)
from src.api_generator.utils.filter_placeholders import filter_placeholders
from src.api_generator.utils.render_template import render_template


class PythonFlaskGenerator(BaseGenerator, Generator):
    def __init__(self):
        super().__init__()
        self.routes_initialized = {
            "GET": False,
            "POST": False,
            "PUT": False,
            "PATCH": False,
            "DELETE": False,
        }

    def initialize(self) -> str:
        self.logger.step("Generate initial boilerplate code")
        return self.store.create(INITIALIZE_TEMPLATE)

    def generate_get(self, id: str, route: str):
        self._generate_route(id, route, "GET", GET_TEMPLATE)

    def generate_post(self, id: str, route: str):
        self._generate_route(id, route, "POST", POST_TEMPLATE)

    def generate_put(self, id: str, route: str):
        self._generate_route(id, route, "PUT", PUT_TEMPLATE)

    def generate_patch(self, id: str, route: str):
        self._generate_route(id, route, "PATCH", PATCH_TEMPLATE)

    def generate_delete(self, id: str, route: str):
        self._generate_route(id, route, "DELETE", DELETE_TEMPLATE)

    def _generate_route(self, id: str, route: str, method: str, template: str):
        self.logger.step(f"Generate {method} method")
        route_name = route.strip("/").replace("/", "_")
        self.append(id, render_template(template, route=route, route_name=route_name))
        self.routes_initialized[method] = True

    def finalize(self, id: str) -> BytesIO:
        self.logger.step("Generate finalize code")
        self.append(id, render_template(FINALIZE_TEMPLATE, host="localhost", port=5000))
        file = self.store.get(id)
        self.update(
            id,
            filter_placeholders(
                file,
                [
                    "new_get_route",
                    "new_post_route",
                    "new_put_route",
                    "new_patch_route",
                    "new_delete_route",
                    "anchor_.*",
                ],
            ),
        )
        self.peek(id)
        file = self.store.get(id)
        self.store.delete(id)
        return file
