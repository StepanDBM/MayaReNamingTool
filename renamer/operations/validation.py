from collections import Counter
from difflib import get_close_matches

from utils.maya_utils import (
    get_selection,
    get_short_name
)


def analyze_selection():

    nodes = get_selection()

    report = {
        "issues": []
    }

    if not nodes:
        return report

    prefixes = []
    suffixes = []

    for node in nodes:

        name = get_short_name(node)

        parts = name.split("_")

        if len(parts) < 2:
            continue

        prefixes.append(parts[0])
        suffixes.append(parts[-1])

    prefix_counter = Counter(prefixes)
    suffix_counter = Counter(suffixes)
    print("PREFIXES:", prefix_counter)
    print("SUFFIXES:", suffix_counter)
    report["issues"].extend(
        find_possible_typos(
            prefix_counter,
            category="prefix"
        )
    )

    report["issues"].extend(
        find_possible_typos(
            suffix_counter,
            category="suffix"
        )
    )

    return report


def find_possible_typos(
    counter,
    category
):

    issues = []

    names = list(counter.keys())

    for name in names:

        if counter[name] > 1:
            continue

        candidates = [
            candidate
            for candidate in names
            if candidate != name
        ]

        matches = get_close_matches(
            name,
            candidates,
            n=1,
            cutoff=0.75
        )

        if not matches:
            continue

        suggestion = matches[0]
        
        if suggestion == name:
            continue

        issues.append(
            {
                "category": category,
                "severity": "warning",
                "name": name,
                "message": "Possible typo",
                "suggestion": suggestion,
            }
        )

    return issues