def build_issue(
    category,
    value,
    message,
    suggestion,
    severity="warning",
    node=None
):

    return {
        "category": category,
        "severity": severity,
        "node": node,
        "value": value,
        "message": message,
        "suggestion": suggestion
    }