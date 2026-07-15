def build_issue(
    category,
    message,
    suggestion,
    severity,
    node=None,
    value=None,
    solver=None,
    solvable=None
):

    issue = {
        "category": category,
        "severity": severity,
        "node": node,
        "value": value,
        "message": message,
        "suggestion": suggestion
    }

    if solver:
        issue["solver"] = solver

    if solvable is not None:
        issue["solvable"] = solvable
    return issue