import numpy as np
from ...utils.config import RESERVED_KEYS


def select_tags(rng, data, p=None):
    """
    Select tags randomly
    String: simply return the tags
    List/dict: choose tags randomly according to the parameters
    (e.g. probability, distribution, etc)
    """

    selected_tags = []

    if isinstance(data, (str, list)):
        data = {"tags": data}

    # Probability
    if p is None:
        p = data.get("probability", 1)

    if rng.random() > p:
        return ""

    # Tag selection
    tags = data.get("tags", [])
    prefix = data.get("prefix", "")
    suffix = data.get("suffix", "")

    if isinstance(tags, str):
        tags = [tags]

    if isinstance(tags, dict):
        if tags.get("tags"):
            tags = select_tags(rng, tags)
        else:
            subtags = []
            for subtag in tags.values():
                subtags.append(select_tags(rng, subtag))
            tags = subtags

    # Number of tags to select
    n = data.get("number", 1)
    if isinstance(n, int) and n > len(tags):
        n = len(tags)

    # If n is a list, choose a
    # random number between the 2 first values
    if isinstance(n, list):
        min_n = n[0]
        max_n = min(n[1], len(tags))
        n = rng.integers(int(min_n), int(max_n))

    # Distribution: how likely each tag is to be selected
    # Normalize the distribution so the sum = 1
    # Add missing values if necessary
    d = data.get("distribution", np.ones(len(tags)))
    if np.sum(d) > 1:
        d = d / np.sum(d)
        d = np.append(d, np.zeros(len(tags) - len(d)))
    elif len(d) < len(tags):
        n_remaining_tags = len(tags) - len(d)
        remaining_d = 1 - np.sum(d)
        d = np.append(
            d, np.full(
                n_remaining_tags,
                remaining_d / n_remaining_tags
            )
        )

    # Chose between the tags
    if tags:
        selected_tags = rng.choice(
            tags,
            size=n,
            p=d,
            replace=False,
        )
        selected_tags = sorted(
            selected_tags, key=lambda x: tags.index(x))

    # Recursive choice (grouped tag)
    else:
        for key, value in data.items():
            if key not in RESERVED_KEYS:
                selected_tags.append(select_tags(rng, value))

    # Add prefix and suffix
    selected_tags = [
        f"{prefix}{tag}{suffix}" for tag in selected_tags
    ]

    # Clean up
    separator = data.get("separator", ",")
    selected_tags = stringify_tags(selected_tags, separator)

    return selected_tags


def stringify_tags(tags, separator=""):
    """
    Return a string from a list of tags
    Remove extra commas and spaces
    """
    if isinstance(tags, np.ndarray):
        tags = tags.tolist()
    tags = separator.join(map(str, tags))

    # Remove extra comma and spaces
    tags = tags.replace(", ", ",").replace(
        ",,", ",").replace(",", ", ").strip(", ")

    return tags
