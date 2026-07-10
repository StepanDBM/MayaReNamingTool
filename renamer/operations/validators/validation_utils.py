def build_issue(
    category,
    value,
    message,
    suggestion,
    severity="warning"
):
    
    return {
        "category": category,
        "severity": severity,
        "value": value,
        "message": message,
        "suggestion": suggestion
    }
