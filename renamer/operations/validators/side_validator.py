from collections import Counter, defaultdict
from importlib import reload

from utils import maya_utils as mUt

from operations.validators import validation_utils as valUtil
from config import namingConventions

reload(namingConventions)


def find_side_naming_issues(nodes):
    issues = []
    namespace_sides = defaultdict(list)
    for node in nodes:
        display_name = mUt.get_short_name(node)
        clean_name = mUt.get_short_name_without_namespace(node)
        namespace = ""
        if ":" in display_name:
            namespace = display_name.rsplit(":", 1)[0]
        parts = clean_name.split("_")
        if not parts:
            continue
        side = parts[0]
        if side not in namingConventions.SIDE_TOKENS:
            continue
        namespace_sides[namespace].append(side)

    for namespace, sides in namespace_sides.items():
        counter = Counter(sides)
        if len(counter) <= 1:
            continue
        prefix = ""
        if namespace:
            prefix = (f"{namespace}: ")
        if "L" in counter and "Left" in counter:
            issues.append(
                valUtil.build_issue(
                    category="side",
                    value=(
                        f"{prefix}L / Left"
                    ),
                    message=(
                        "Mixed left-side naming convention"
                    ),
                    suggestion=(
                        "Use either L or Left consistently"
                    ),
                    severity="warning"
                )
            )
        if "R" in counter and "Right" in counter:
            issues.append(
                valUtil.build_issue(
                    category="side",
                    value=(
                        f"{prefix}R / Right"
                    ),
                    message=(
                        "Mixed right-side naming convention"
                    ),
                    suggestion=(
                        "Use either R or Right consistently"
                    ),
                    severity="warning"
                )
            )
    return issues