from importlib import reload

from utils import maya_utils as mUt

from operations.validators import typo_validator
from operations.validators import numbering_validator
from operations.validators import default_name_validator
from operations.validators import underscore_valdiator
from operations.validators import side_validator
from operations.validators import unknown_suffix_validator
from operations.validators import duplicate_name_validator
from operations.validators import type_validator
from operations.validators import missing_suffix_validator
from operations.validators import consistent_padding_validator
from operations.validators import unkown_prefix_validator
from operations.validators import empty_group_validator
from operations.validators import token_count_validator


def analyze_selection():
    #refactoed for debugging purposes in Maya's hot runtime python package reload -.-
    reload(typo_validator)
    reload(numbering_validator)
    reload(default_name_validator)
    reload(underscore_valdiator)
    reload(side_validator)
    reload(unknown_suffix_validator)
    reload(duplicate_name_validator)
    reload(type_validator)
    reload(missing_suffix_validator)
    reload(consistent_padding_validator)
    reload(unkown_prefix_validator)
    reload(empty_group_validator)
    reload(token_count_validator)

    nodes = mUt.get_naming_nodes()

    if not nodes:
        nodes = mUt.get_all_naming_nodes()

    if not nodes:
        return report


    report = {
        "issues": []
    }

    if not nodes:
        return report

    report["issues"].extend(
        typo_validator.find_possible_typo_issues(nodes)
    )
    report["issues"].extend(
        numbering_validator.find_numbering_issues(nodes)
    )
    report["issues"].extend(
        default_name_validator.find_default_name_issues(nodes)
    )
    report["issues"].extend(
        underscore_valdiator.find_double_underscore_issues(nodes)
    )
    report["issues"].extend(
        underscore_valdiator.find_empty_token_issues(nodes)
    )
    report["issues"].extend(
        side_validator.find_side_naming_issues(nodes)
    )
    report["issues"].extend(
        unknown_suffix_validator.find_unknown_suffix_issues(nodes)
    )
    report["issues"].extend(
        duplicate_name_validator.find_duplicate_name_issues(nodes)
    )
    report["issues"].extend(
        type_validator.find_type_issues(nodes)
    )
    report["issues"].extend(
        missing_suffix_validator.find_missing_suffix_issues(nodes)
    )
    report["issues"].extend(
        consistent_padding_validator.find_padding_issues(nodes)
    )
    report["issues"].extend(
        unkown_prefix_validator.find_unknown_prefix_issues(nodes)
    )
    report["issues"].extend(
        empty_group_validator.find_empty_group_issues(nodes)
    )
    report["issues"].extend(
        token_count_validator.find_token_count_issues(nodes)
    )

    print(report)

    return report