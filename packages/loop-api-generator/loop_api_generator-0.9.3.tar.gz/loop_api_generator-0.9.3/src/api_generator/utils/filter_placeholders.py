import re


def filter_placeholders(text: str, placeholders: list[str]) -> str:
    for placeholder in placeholders:
        text = re.sub(r"\{\{\s*" + placeholder + r"\s*\}\}", "", text)
    return text
