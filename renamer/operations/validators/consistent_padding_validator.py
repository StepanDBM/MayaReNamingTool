from collections import defaultdict

from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


def find_padding_issues(nodes):

    issues = []

    families = defaultdict(set)

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        for index, part in enumerate(parts):

            if not part.isdigit():
                continue

            family_parts = parts[:]
            family_parts[index] = "*"

            family = "_".join(
                family_parts
            )

            families[family].add(
                len(part)
            )

            break

    for family, paddings in families.items():

        if len(paddings) <= 1:
            continue

        issues.append(
            valUtil.build_issue(
                category="numbering",
                value=family,
                message="Inconsistent number padding",
                suggestion=(
                    f"Found padding sizes: "
                    f"{sorted(paddings)}"
                )
            )
        )

    return issues