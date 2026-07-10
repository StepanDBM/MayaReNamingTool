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

    prefix_nodes = {}
    suffix_nodes = {}

    for node in nodes:

        node_name = mUt.get_short_name(node)

        parts = node_name.split("_")

        if len(parts) < 2:
            continue

        prefix = parts[0]
        suffix = parts[-1]

        prefixes.append(prefix)
        suffixes.append(suffix)

        prefix_nodes[prefix] = node_name
        suffix_nodes[suffix] = node_name

    prefix_counter = Counter(
        prefixes
    )

    suffix_counter = Counter(
        suffixes
    )

    issues.extend(
        _find_possible_typos(
            prefix_counter,
            prefix_nodes,
            category="prefix"
        )
    )

    issues.extend(
        _find_possible_typos(
            suffix_counter,
            suffix_nodes,
            category="suffix"
        )
    )

    return issues


def _find_possible_typos(
    counter,
    node_lookup,
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
                node=node_lookup.get(name),
                value=name,
                message="Possible typo",
                suggestion=suggestion,
                severity="warning"
            )
        )

    return issues