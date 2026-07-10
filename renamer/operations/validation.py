from collections import Counter
from difflib import get_close_matches

from utils.maya_utils import (
    get_selection,
    get_short_name
)


def analyze_selection():

    nodes = get_selection()

    report = {
        "prefixes": {},
        "suffixes": {},
        "warnings": []
    }

    if not nodes:
        return report

    prefixes = []
    suffixes = []

    for node in nodes:

        name = get_short_name(node)

        parts = name.split("_")

        if len(parts) >= 2:

            prefixes.append(parts[0])

            suffixes.append(parts[-1])

    prefix_counter = Counter(prefixes)
    suffix_counter = Counter(suffixes)

    report["prefixes"] = dict(prefix_counter)
    report["suffixes"] = dict(suffix_counter)

    warnings = []

    warnings.extend(
        find_possible_typos(prefix_counter)
    )

    warnings.extend(
        find_possible_typos(suffix_counter)
    )

    report["warnings"] = warnings

    return report


def find_possible_typos(counter):

    warnings = []

    names = list(counter.keys())

    for name in names:

        if counter[name] > 1:
            continue

        matches = get_close_matches(
            name,
            names,
            n=1,
            cutoff=0.75
        )

        if not matches:
            continue

        suggestion = matches[0]

        if suggestion == name:
            continue

        warnings.append(
            f"Possible typo: '{name}' -> '{suggestion}'"
        )

    return warnings