from uuid import uuid4


def generate_uuid() -> str:
    """
    Generate a UUID string

    :return: UUID string
    """
    return str(uuid4())
