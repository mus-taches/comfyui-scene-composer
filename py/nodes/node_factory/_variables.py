from ._tags import choose_random_tags


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

    if isinstance(tags, str):
        return [replace_placeholders(tags, variables)]

    replaced_tags = {}
    for key, value in tags.items():

        # Loop until all placeholder are replaced
        while any("{" + placeholder + "}" in value for placeholder in variables.keys()):
            value = replace_placeholders(value, variables)
        replaced_tags[key] = value

    return replaced_tags
