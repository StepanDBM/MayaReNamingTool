from collections import Counter

from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


def find_duplicate_name_issues(nodes):

    issues = []

    short_names = []

    for node in nodes:

        short_names.append(
            mUt.get_short_name(node)
        )

    counter = Counter(
        short_names
    )

    for name, count in counter.items():

        if count < 2:
            continue

        issues.append(
            valUtil.build_issue(
                category="duplicate_name",
                value=name,
                message="Duplicate short name detected",
                suggestion=(
                    f"Found {count} nodes with this name"
                )
            )
        )

    return issues