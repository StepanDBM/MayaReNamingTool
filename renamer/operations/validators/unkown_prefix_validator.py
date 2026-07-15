from collections import Counter
from difflib import get_close_matches
from utils import maya_utils as mUt
from operations.validators import validation_utils as valUtil

KNOWN_PREFIXES = {
    "char",
    "character",
    "vehicle",
    "prop",
    "tentacle",
    "rope",
    "L",
    "R",
    "Left",
    "Right"
}

def find_unknown_prefix_issues(nodes):
    issues = []
    prefixes = []
    prefix_nodes = {}

    for node in nodes:
        display_name = mUt.get_short_name(node)
        clean_name = mUt.get_short_name_without_namespace(node)
        parts = clean_name.split("_")
        if "" in parts:
            continue
        if len(parts) < 2:
            continue
        prefix = parts[0]
        prefixes.append(
            prefix
        )
        prefix_nodes.setdefault(prefix, display_name)
    counter = Counter(prefixes)
    all_prefixes = list(counter.keys())

    for prefix in counter:
        if prefix in KNOWN_PREFIXES:
            continue

        # Let typo validator handle this.
        matches = get_close_matches(
            prefix,
            [
                candidate
                for candidate in all_prefixes
                if (
                    candidate != prefix
                    and counter[candidate] > counter[prefix]
                )
            ],
            n=1,
            cutoff=0.75
        )

        if matches:
            continue

        issues.append(
            valUtil.build_issue(
                category="prefix",
                node=prefix_nodes.get(
                    prefix
                ),
                value=prefix,
                message="Unknown prefix",
                suggestion="Use a known prefix",
                severity="warning"
            )
        )

    return issues