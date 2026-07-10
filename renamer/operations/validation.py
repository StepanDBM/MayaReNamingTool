from collections import Counter, defaultdict
from difflib import get_close_matches

from utils import maya_utils as mUt

from utils import infoFormatting as infoForm


def analyze_selection():

    nodes = mUt.get_naming_nodes()

    report = {
        "issues": []
    }

    if not nodes:
        return report

    prefixes = []
    suffixes = []

    for node in nodes:

        name = mUt.get_short_name(node)

        parts = name.split("_")

        if len(parts) < 2:
            continue

        prefixes.append(parts[0])
        suffixes.append(parts[-1])

    prefix_counter = Counter(prefixes)
    suffix_counter = Counter(suffixes)
    report["issues"].extend(
        find_possible_typos(
            prefix_counter,
            category="prefix"
        )
    )

    report["issues"].extend(
        find_possible_typos(
            suffix_counter,
            category="suffix"
        )
    )
    report["issues"].extend(
        find_numbering_issues(nodes)
    )
    print(report)

    return report


def find_possible_typos(
    counter,
    category
):

    issues = []

    names = list(counter.keys())

    for name in names:

        if counter[name] > 1:
            continue

        candidates = [
            candidate
            for candidate in names
            if candidate != name
        ]

        matches = get_close_matches(
            name,
            candidates,
            n=1,
            cutoff=0.75
        )

        if not matches:
            continue

        suggestion = matches[0]
        
        if suggestion == name:
            continue

        issues.append(
            {
                "category": category,
                "severity": "warning",
                "value": name,
                "message": "Possible typo",
                "suggestion": suggestion,
            }
        )

    return issues

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
            {
                "category": "numbering",
                "severity": "warning",
                "value": family,
                "message": "Missing numbering sequence",
                "suggestion": infoForm.format_number_ranges(missing)
            }
        )

    return issues