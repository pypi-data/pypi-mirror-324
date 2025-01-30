from io import BytesIO


def text_to_buffer(content: str) -> BytesIO:
    """
    Converts a string into a BytesIO buffer using UTF-8 encoding.

    Args:
        content (str): The string content to be converted.

    Returns:
        BytesIO: A buffer containing the UTF-8 encoded bytes
        of the input string.
    """
    return BytesIO(content.encode("utf-8"))
