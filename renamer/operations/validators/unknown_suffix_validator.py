from collections import Counter
from difflib import get_close_matches

from utils import maya_utils as mUt
from utils.loaders import loadNamingRules as N_Rules

from operations.validators import validation_utils as valUtil


def find_unknown_suffix_issues(nodes):

    issues = []

    suffixes = []
    suffix_nodes = {}

    rules = N_Rules.load_rules()
    valid_suffixes = set(rules.get("suffixes", []))

    for node in nodes:

        display_name = mUt.get_short_name(node)
        clean_name = mUt.get_short_name_without_namespace(node)

        parts = clean_name.split("_")

        if "" in parts:
            continue

        # Two-token names like char_helmet are missing suffix,
        # not unknown suffix.
        if len(parts) < 3:
            continue

        suffix = parts[-1]

        suffixes.append(suffix)
        suffix_nodes.setdefault(suffix, display_name)

    counter = Counter(suffixes)
    all_suffixes = list(counter.keys())

    for suffix in counter:

        if suffix in valid_suffixes:
            continue

        # If it looks like a typo, let typo_validator handle it.
        matches = get_close_matches(
            suffix,
            [
                candidate
                for candidate in all_suffixes
                if (
                    candidate != suffix
                    and counter[candidate] > counter[suffix]
                )
            ],
            n=1,
            cutoff=0.75
        )

        if matches:
            continue

        issues.append(
            valUtil.build_issue(
                category="suffix",
                node=suffix_nodes.get(suffix),
                value=suffix,
                message="Unknown suffix",
                suggestion="Use a known suffix",
                severity="warning",
                solvable=False
            )
        )

    return issues