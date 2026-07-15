from collections import defaultdict
from utils import maya_utils as mUt
from operations.validators import validation_utils as valUtil


def find_duplicate_name_issues(nodes):
    issues = []
    clean_name_nodes = defaultdict(list)

    for node in nodes:
        display_name = mUt.get_short_name(node)
        clean_name = (mUt.get_short_name_without_namespace(node))
        clean_name_nodes[clean_name].append(display_name)

    for clean_name, matching_nodes in clean_name_nodes.items():
        count = len(matching_nodes)
        if count < 2:
            continue

        example_node = matching_nodes[0]
        issues.append(
            valUtil.build_issue(
                category="duplicate_name",
                node=example_node,
                value=clean_name,
                message="Duplicate clean name detected",
                suggestion=(
                    f"Found {count} nodes that resolve "
                    f"to '{clean_name}'"
                ),
                severity="error"
            )
        )

    return issues