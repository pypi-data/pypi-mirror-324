import re
from io import BytesIO

from src.api_generator.generator.base_generator import BaseGenerator
from src.api_generator.generator.generator import Generator
from src.api_generator.generator.python.templates import (
    DELETE_ROUTE_TEMPLATE,
    DELETE_TEMPLATE,
    FINALIZE_TEMPLATE,
    GET_ROUTE_TEMPLATE,
    GET_TEMPLATE,
    INITIALIZE_TEMPLATE,
    PATCH_ROUTE_TEMPLATE,
    PATCH_TEMPLATE,
    POST_ROUTE_TEMPLATE,
    POST_TEMPLATE,
    PUT_ROUTE_TEMPLATE,
    PUT_TEMPLATE,
)
from src.api_generator.utils.filter_placeholders import filter_placeholders
from src.api_generator.utils.render_template import render_template


class PythonGenerator(BaseGenerator, Generator):
    def __init__(self):
        super().__init__()
        self.__init_get = False
        self.__init_post = False
        self.__init_put = False
        self.__init_patch = False
        self.__init_delete = False

    def initialize(self) -> str:
        self.logger.step("Generate inital boilerplate code")
        return self.store.create(INITIALIZE_TEMPLATE)

    def generate_get(self, id: str, route: str):
        self.logger.step("Generate GET method")
        if not self.__init_get:
            self.append(id, render_template(GET_TEMPLATE, route=route))
            self.__init_get = True
        else:
            anchor_points_count = len(
                re.findall(
                    r"\{\{\s*anchor_get_route_\d+_begin\s*\}\}", self.store.get(id)
                )
            )
            self.update(
                id,
                render_template(
                    self.store.get(id),
                    new_get_route=render_template(
                        GET_ROUTE_TEMPLATE,
                        route=route,
                        anchor_get_route_begin="{{ "
                        + f"anchor_get_route_{anchor_points_count}_begin"
                        + " }}",
                        anchor_get_route_end="{{ "
                        + f"anchor_get_route_{anchor_points_count}_end"
                        + " }}",
                    ),
                ),
            )

    def generate_post(self, id: str, route: str):
        self.logger.step("Generate POST method")
        if not self.__init_post:
            self.append(id, render_template(POST_TEMPLATE, route=route))
            self.__init_post = True
        else:
            anchor_points_count = len(
                re.findall(
                    r"\{\{\s*anchor_post_route_\d+_begin\s*\}\}", self.store.get(id)
                )
            )
            self.update(
                id,
                render_template(
                    self.store.get(id),
                    new_post_route=render_template(
                        POST_ROUTE_TEMPLATE,
                        route=route,
                        anchor_post_route_begin="{{ "
                        + f"anchor_post_route_{anchor_points_count}_begin"
                        + " }}",
                        anchor_post_route_end="{{ "
                        + f"anchor_post_route_{anchor_points_count}_end"
                        + " }}",
                    ),
                ),
            )

    def generate_put(self, id: str, route: str):
        self.logger.step("Generate PUT method")
        if not self.__init_put:
            self.append(id, render_template(PUT_TEMPLATE, route=route))
            self.__init_put = True
        else:
            anchor_points_count = len(
                re.findall(
                    r"\{\{\s*anchor_put_route_\d+_begin\s*\}\}", self.store.get(id)
                )
            )
            self.update(
                id,
                render_template(
                    self.store.get(id),
                    new_put_route=render_template(
                        PUT_ROUTE_TEMPLATE,
                        route=route,
                        anchor_put_route_begin="{{ "
                        + f"anchor_put_route_{anchor_points_count}_begin"
                        + " }}",
                        anchor_put_route_end="{{ "
                        + f"anchor_put_route_{anchor_points_count}_end"
                        + " }}",
                    ),
                ),
            )

    def generate_patch(self, id: str, route: str):
        self.logger.step("Generate PATCH method")
        if not self.__init_patch:
            self.append(id, render_template(PATCH_TEMPLATE, route=route))
            self.__init_patch = True
        else:
            anchor_points_count = len(
                re.findall(
                    r"\{\{\s*anchor_patch_route_\d+_begin\s*\}\}", self.store.get(id)
                )
            )
            self.update(
                id,
                render_template(
                    self.store.get(id),
                    new_patch_route=render_template(
                        PATCH_ROUTE_TEMPLATE,
                        route=route,
                        anchor_patch_route_begin="{{ "
                        + f"anchor_patch_route_{anchor_points_count}_begin"
                        + " }}",
                        anchor_patch_route_end="{{ "
                        + f"anchor_patch_route_{anchor_points_count}_end"
                        + " }}",
                    ),
                ),
            )

    def generate_delete(self, id: str, route: str):
        self.logger.step("Generate DELETE method")
        if not self.__init_delete:
            self.append(id, render_template(DELETE_TEMPLATE, route=route))
            self.__init_delete = True
        else:
            anchor_points_count = len(
                re.findall(
                    r"\{\{\s*anchor_delete_route_\d+_begin\s*\}\}", self.store.get(id)
                )
            )
            self.update(
                id,
                render_template(
                    self.store.get(id),
                    new_delete_route=render_template(
                        DELETE_ROUTE_TEMPLATE,
                        route=route,
                        anchor_delete_route_begin="{{ "
                        + f"anchor_delete_route_{anchor_points_count}_begin"
                        + " }}",
                        anchor_delete_route_end="{{ "
                        + f"anchor_delete_route_{anchor_points_count}_end"
                        + " }}",
                    ),
                ),
            )

    def finalize(self, id: str) -> BytesIO:
        self.logger.step("Generate finalize code")
        self.append(id, render_template(FINALIZE_TEMPLATE, host="localhost", port=8080))
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
