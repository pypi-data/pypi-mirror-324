from io import BytesIO

from api_generator.generator.base_generator import BaseGenerator
from api_generator.generator.generator import Generator
from api_generator.generator.python_bottle.templates import (
    DELETE_TEMPLATE,
    FINALIZE_TEMPLATE,
    GET_TEMPLATE,
    INITIALIZE_TEMPLATE,
    PATCH_TEMPLATE,
    POST_TEMPLATE,
    PUT_TEMPLATE,
)
from api_generator.utils.filter_placeholders import filter_placeholders
from api_generator.utils.render_template import render_template


class PythonBottleGenerator(BaseGenerator, Generator):
    def __init__(self):
        super().__init__()

    def initialize(self) -> str:
        self.logger.step("Generate inital boilerplate code")
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

    def finalize(self, id: str) -> BytesIO:
        self.logger.step("Generate finalize code")
        self.append(id, render_template(FINALIZE_TEMPLATE, host="localhost", port=8080))
        file = self.store.get(id)

        (
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
            ),
        )
        self.peek(id)

        self.store.delete(id)
        return file
