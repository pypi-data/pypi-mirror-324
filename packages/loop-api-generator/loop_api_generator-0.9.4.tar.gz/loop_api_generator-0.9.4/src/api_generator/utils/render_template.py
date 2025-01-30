def render_template(template: str, **kwargs) -> str:
    """
    Renders a template string by replacing placeholders with provided keyword arguments.

    Args:
        template (str): The template string containing placeholders in the format
        {{ key }}.
        **kwargs: Arbitrary keyword arguments where the key corresponds to the
        placeholder in the template and the value is the value to replace
        the placeholder with.

    Returns:
        str: The rendered template string with all placeholders replaced by their
        corresponding values.

    Example:
        render_template("Hello {{ placeholder }}", placeholder="World") -> "Hello World"
    """
    for key, value in kwargs.items():
        template = template.replace("{{ " + key + " }}", str(value))
    return template
