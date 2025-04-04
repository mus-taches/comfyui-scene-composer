import dpath.util as dpath


def build_inputs(self):
    "Build node's inputs according to the data"
    inputs = {"required": {}, "optional": {}}

    if self.data.get("hide", False):
        return inputs

    variables_inputs = process_inputs(self.data.get("variables", {}))
    tags_inputs = process_inputs(self.data.get("tags", {}))

    inputs["required"] = {**variables_inputs, **tags_inputs}
    return inputs


def process_inputs(data):
    inputs = {}
    for key, value in dpath.search(data, '*', yielded=True):

        inputs[key] = format_value(key, value)
        if inputs[key] is None:
            inputs.pop(key)
            continue

        input_type = inputs[key][0]
        if input_type in ("FLOAT", "BOOLEAN"):
            inputs[f"{key}?"] = inputs.pop(key)

    return inputs


def format_value(key, value):
    "Format the value to respect ComfyUI's convention, depending on the type"

    input = None

    match value:

        case bool():
            input = ("BOOLEAN", {
                "default": value
            })

        case float():
            input = ("FLOAT", {
                "default": value,
                "min": 0,
                "max": 1,
                "step": 0.05
            })

        case str():
            input = ("STRING", {
                "default": value,
                "multiline": True
            })

        case list():
            items_are_strings = all(isinstance(item, str) for item in value)
            if items_are_strings:
                value = ["random", *value, "none"]

            input = (value, {
                "default": value[0] if value else ""
            })

        case dict():

            conditions = [
                value.get("hide", False),
                "tags" not in value
            ]

            if any(conditions):
                return

            match value["tags"]:

                case list() | str():
                    input = format_value(key, value["tags"])

                case dict():
                    input = format_subtags(key, value)

    return input


def format_subtags(key, value):
    """
    Handle how subtags/group of tags are displayed as input in the node,
    depending on the config file
    """

    display_group_labels = value.get("group_labels", False)
    probability_key = value.get("probability", 1)

    # Display true/false checkbox as input
    input = format_value(key, True)

    # Display subtags labels as input
    if display_group_labels:
        tags_keys = list(value["tags"].keys())
        input = format_value(key, tags_keys)

    # Display a custom probability is set, show a float as input
    if probability_key != 1:
        input = format_value(key, probability_key)

    return input


def apply_input_values(data, inputs):
    """
    Apply what has been selected in the node inputs
    Can be "random", "none", or a selected value
    """
    applied_values = {}

    # Remove "?" from keys in inputs
    inputs = {key.rstrip('?'): value for key, value in inputs.items()}

    def traverse(data):

        for key, value in data.items():

            selected = inputs.get(key, "random")
            match selected:

                # If "none" or false, just ignore the tag
                case "none" | False:
                    applied_values[key] = ""

                # If a number, use "probability"
                case int() | float():
                    if isinstance(value, dict) and "probability" in value:
                        value["probability"] = selected
                    applied_values[key] = value

                # If "random", return the string, list or dict
                # according to the JSON config file
                case "random":
                    applied_values[key] = value

                    if isinstance(value, dict) and not value.get("tags"):
                        traverse(value)

                # If a value is selected, just return it
                case _:
                    applied_values[key] = selected

                    if selected is True:
                        applied_values[key] = value
                        continue

                    if isinstance(value, dict):
                        prefix = value.get("prefix", "")
                        suffix = value.get("suffix", "")
                        applied_values[key] = f"{prefix}{selected}{suffix}"

                        if isinstance(value.get("tags"), dict):
                            applied_values[key] = value["tags"][selected]

    traverse(data)
    return applied_values
