from utils import maya_utils as mUt

from operations.validators.typo_validator import (
    find_possible_typo_issues
)

from operations.validators.numbering_validator import (
    find_numbering_issues
)


def analyze_selection():

    nodes = mUt.get_naming_nodes()

    report = {
        "issues": []
    }

    if not nodes:
        return report

    report["issues"].extend(
        find_possible_typo_issues(nodes)
    )

    report["issues"].extend(
        find_numbering_issues(nodes)
    )

    print(report)

    return report