from io import BytesIO

from api_generator.generator.base_generator import BaseGenerator
from api_generator.generator.fast_api.templates import (
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


class FastAPIGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.__init_boilerplate = False

    def initialize(self) -> str:
        """
        Tworzy początkowy kod aplikacji FastAPI.
        """
        self.logger.step("Generating initial FastAPI boilerplate")
        return self.store.create(INITIALIZE_TEMPLATE)

    def _generate_method(self, id: str, route: str, template: str, method_name: str):
        """
        Generuje trasę HTTP dla dowolnej metody.
        """
        self.logger.step(f"Generating {method_name.upper()} method for route: {route}")
        rendered_method = render_template(
            template,
            route=route,
            route_safe=route.replace("/", "_"),
        )
        self.append(id, rendered_method)

    def generate_get(self, id: str, route: str):
        self._generate_method(id, route, GET_TEMPLATE, "GET")

    def generate_post(self, id: str, route: str):
        self._generate_method(id, route, POST_TEMPLATE, "POST")

    def generate_put(self, id: str, route: str):
        self._generate_method(id, route, PUT_TEMPLATE, "PUT")

    def generate_patch(self, id: str, route: str):
        self._generate_method(id, route, PATCH_TEMPLATE, "PATCH")

    def generate_delete(self, id: str, route: str):
        self._generate_method(id, route, DELETE_TEMPLATE, "DELETE")

    def finalize(self, id: str, host: str = "localhost", port: int = 8000) -> BytesIO:
        """
        Generuje końcowy kod FastAPI i przygotowuje go do użycia.
        """
        self.logger.step("Generating finalize code for FastAPI")
        finalize_code = render_template(FINALIZE_TEMPLATE, host=host, port=port)
        self.append(id, finalize_code)
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
