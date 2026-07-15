from difflib import get_close_matches

from utils import maya_utils as mUt
from utils.loaders import loadNamingRules as N_Rules

from operations.validators import validation_utils as valUtil


def find_missing_suffix_issues(nodes):

    issues = []

    rules = N_Rules.load_rules()
    known_suffixes = set(rules.get("suffixes", []))

    for node in nodes:

        display_name = mUt.get_short_name(node)
        clean_name = mUt.get_short_name_without_namespace(node)

        parts = clean_name.split("_")

        if "" in parts:
            continue

        if len(parts) < 2:
            continue

        suffix = parts[-1]

        if suffix in known_suffixes:
            continue

        # If it already has 3+ tokens, it has a suffix slot.
        # It may be wrong/unknown/typo, but it is not missing.
        if len(parts) >= 3:
            continue

        matches = get_close_matches(
            suffix,
            list(known_suffixes),
            n=1,
            cutoff=0.75
        )

        if matches:
            continue

        issues.append(
            valUtil.build_issue(
                category="suffix",
                node=display_name,
                value=clean_name,
                message="Missing naming suffix",
                suggestion="Add a valid suffix",
                severity="warning",
                solvable=False
            )
        )

    return issues