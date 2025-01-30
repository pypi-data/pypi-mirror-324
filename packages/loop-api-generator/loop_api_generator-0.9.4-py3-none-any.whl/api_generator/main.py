from . import (
    ExpressJSGenerator,
    FastAPIGenerator,
    PythonBottleGenerator,
    PythonFlaskGenerator,
    PythonGenerator,
)

if __name__ == "__main__":
    python = PythonGenerator()
    fastapi = FastAPIGenerator()
    flask = PythonFlaskGenerator()
    express = ExpressJSGenerator()
    bottle = PythonBottleGenerator()

    generator = bottle

    id = generator.initialize()

    generator.generate_get(id, "v1")
    generator.generate_post(id, "v1")
    generator.generate_put(id, "v1")
    generator.generate_patch(id, "v1")
    generator.generate_delete(id, "v1")

    generator.generate_get(id, "v2")
    generator.generate_post(id, "v2")
    generator.generate_put(id, "v2")
    generator.generate_patch(id, "v2")
    generator.generate_delete(id, "v2")

    generator.generate_get(id, "v3")
    generator.generate_get(id, "v4")

    final_code = generator.finalize(id)
