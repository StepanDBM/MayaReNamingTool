from importlib import reload
from collections import Counter
from difflib import get_close_matches

from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil
reload(valUtil)


def find_possible_typo_issues(nodes):

    issues = []

    prefixes = []
    suffixes = []

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if len(parts) < 2:
            continue

        prefixes.append(
            parts[0]
        )

        suffixes.append(
            parts[-1]
        )

    prefix_counter = Counter(
        prefixes
    )

    suffix_counter = Counter(
        suffixes
    )

    issues.extend(
        _find_possible_typos(
            prefix_counter,
            category="prefix"
        )
    )

    issues.extend(
        _find_possible_typos(
            suffix_counter,
            category="suffix"
        )
    )

    return issues


def _find_possible_typos(
    counter,
    category
):

    issues = []

    names = list(
        counter.keys()
    )

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
            valUtil.build_issue(
                category=category,
                value=name,
                message="Possible typo",
                suggestion=suggestion
            )
        )

    return issues