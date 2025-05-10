from ._tags import choose_random_tags
from ...components.blackboard import Blackboard


def apply_variables(rng, tags, variables):
    """
    Each time a {variable} placeholder is found in `tags`, it will be replaced with a value in `variables` which has the same key.
    """

    def replace_placeholders(text, variables):

        if isinstance(text, dict):
            text = choose_random_tags(rng, text)

        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            while placeholder in text:
                replacement = choose_random_tags(rng, value)
                text = text.replace(placeholder, str(replacement), 1)

        return text

    def process_placeholders(item):
        while any("{" + placeholder + "}" in item for placeholder in variables.keys()):
            item = replace_placeholders(item, variables)
        return item

    replaced_tags = {}

    if isinstance(tags, str):
        return [process_placeholders(tags)]

    if isinstance(tags, list):
        for tag in tags:
            replaced_tags[tag] = process_placeholders(tag)
        return list(replaced_tags.values())

    for key, value in tags.items():
        if isinstance(value, str):
            replaced_tags[key] = process_placeholders(value)
        else:
            replaced_tags[key] = value

    return replaced_tags


def spread_variables(text):
    variables = Blackboard().variables
    text_has_changed = False

    if text.startswith("{") and text.endswith("}"):
        placeholder = text[1:-1]
        if placeholder in variables:
            text_has_changed = True
            text = variables[placeholder]

    return text_has_changed, text
