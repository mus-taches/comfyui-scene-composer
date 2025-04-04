from ...utils.config import load_config
from ._tags import select_tags


def load_variables(rng, data):
    "Load global and local variables from config files"

    global_variables = load_config("variables", with_filename=False)

    # Replace local variables with value from global variables
    local_variables = process_variables(rng, data)
    local_variables = apply_variables(rng, local_variables, global_variables)

    # Merge global and local variables
    variables = {**global_variables, **local_variables}
    variables = process_variables(rng, variables)
    return variables


def process_variables(rng, variables):
    "Process variable with list and dict"
    for key, value in variables.items():
        if isinstance(value, dict) and not value.get("fixed", True):
            variables[key] = value.get("tags", [])
            continue
        variables[key] = select_tags(rng, value)
    return variables


def apply_variables(rng, tags, variables):
    "Replace tags with {variables} with corresponding variable"

    def replace_variables(text, variables):
        for var_key, var_value in variables.items():
            count = text.count("{" + var_key + "}")
            for _ in range(count):
                var_value = select_tags(rng, variables[var_key])
                text = text.replace("{" + var_key + "}", f"{var_value}", 1)
        return text

    if isinstance(tags, str):
        return [replace_variables(tags, variables)]

    replaced_tags = {}
    for key, value in tags.items():
        replaced_tags[key] = replace_variables(value, variables)

    return replaced_tags
