from collections import Counter, defaultdict

from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


def find_token_count_issues(nodes):
    issues = []
    families = defaultdict(list)
    for node in nodes:
        display_name = mUt.get_short_name(node)
        clean_name = mUt.get_short_name_without_namespace(node)
        parts = clean_name.split("_")
        if len(parts) < 2:
            continue
        if "" in parts:
            continue
        family = parts[0]
        families[family].append(
            (
                display_name,
                clean_name,
                len(parts)
            )
        )

    for family, entries in families.items():
        counts = [
            token_count
            for _, _, token_count in entries
        ]
        expected = Counter(
            counts
        ).most_common(1)[0][0]
        for display_name, clean_name, token_count in entries:
            if token_count == expected:
                continue
            issues.append(
                valUtil.build_issue(
                    category="structure",
                    node=display_name,
                    value=clean_name,
                    message="Unexpected token count",
                    suggestion=(
                        f"Expected {expected} tokens, "
                        f"found {token_count}"
                    ),
                    severity="mind_me"
                )
            )

    return issues