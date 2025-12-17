def needs_personality(query: str) -> bool:
    q = query.lower()
    return any(
        word in q
        for word in [
            "collaborat",
            "communication",
            "team",
            "business",
            "stakeholder",
            "customer",
            "interpersonal",
            "behavior",
            "culture",
        ]
    )
