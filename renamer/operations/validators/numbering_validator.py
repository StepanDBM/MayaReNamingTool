from importlib import reload
from collections import defaultdict

from utils import maya_utils as mUt
from utils import infoFormatting as infoForm


from operations.validators import validation_utils as valUtil
reload(valUtil)


def find_numbering_issues(nodes):

    issues = []

    families = defaultdict(list)

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

            families[family].append(
                int(part)
            )

            break

    for family, numbers in families.items():

        if len(numbers) < 2:
            continue

        numbers = sorted(
            set(numbers)
        )

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

        issues.append(
            valUtil.build_issue(
                category="numbering",
                node = name,
                value=family,
                message="Missing numbering sequence",
                suggestion=infoForm.format_number_ranges(
                    missing
                ),
                severity="warning"
            )
        )

    return issues