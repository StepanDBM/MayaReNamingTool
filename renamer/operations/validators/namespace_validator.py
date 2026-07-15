from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil


def find_namespace_issues(nodes):

    issues = []

    seen = set()

    for node in nodes:

        display_name = mUt.get_short_name(node)

        if ":" not in display_name:
            continue

        namespace, clean_name = display_name.rsplit(":", 1)

        key = (namespace, display_name)

        if key in seen:
            continue

        seen.add(key)

        issues.append(
            valUtil.build_issue(
                category="namespace",
                node=display_name,
                value=namespace,
                message="Namespace detected",
                suggestion=(
                    f"Strip namespace to use "
                    f"'{clean_name}'"
                ),
                severity="warning",
                solver="strip_namespace",
                solvable=True
            )
        )

    return issues