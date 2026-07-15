from importlib import reload
from collections import defaultdict

from utils import maya_utils as mUt
from utils import infoFormatting as infoForm

from operations.validators import validation_utils as valUtil

reload(valUtil)

"""
diferent referenced objects/rigs are treatted as separated famliies and as such,
do not pollute with weird naming conventions between each other.
"""
def find_numbering_issues(nodes):
    issues = []
    families = defaultdict(list)
    family_display_names = {}

    for node in nodes:
        display_name = mUt.get_short_name(node)
        clean_name = (mUt.get_short_name_without_namespace(node))
        namespace = ""
        if ":" in display_name:
            namespace = display_name.rsplit(":", 1)[0]

        parts = clean_name.split("_")

        for index, part in enumerate(parts):

            if not part.isdigit():
                continue

            family_parts = parts[:]
            family_parts[index] = "*"
            family = "_".join(family_parts)
            family_key = (namespace, family)

            if namespace:
                display_family = (f"{namespace}:{family}")
            else:
                display_family = family
            families[family_key].append(int(part))
            family_display_names.setdefault(family_key, display_family)
            break

    for family_key, numbers in families.items():
        if len(numbers) < 2:
            continue
        numbers = sorted(set(numbers))
        expected = range(
            numbers[0],
            numbers[-1] + 1
        )

        missing = [
            number
            for number in expected
            if number not in numbers
        ]

        if not missing:
            continue

        family_display = family_display_names[family_key]

        issues.append(
            valUtil.build_issue(
                category="numbering",
                node=family_display,
                value=family_display,
                message="Missing numbering sequence",
                suggestion=infoForm.format_number_ranges(
                    missing
                ),
                severity="warning"
            )
        )

    return issues