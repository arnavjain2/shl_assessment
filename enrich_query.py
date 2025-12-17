def enrich_query(query: str) -> str:
    q = query.lower()

    extra_terms = []

    if "java" in q:
        extra_terms += ["java", "programming", "software development"]

    if "python" in q:
        extra_terms += ["python", "coding"]

    if "sales" in q:
        extra_terms += ["sales", "customer interaction", "communication"]

    if "collaborat" in q or "team" in q:
        extra_terms += ["interpersonal", "communication", "teamwork"]

    if "entry" in q or "graduate" in q:
        extra_terms += ["entry level", "junior"]

    if "manager" in q:
        extra_terms += ["leadership", "management"]

    if "personality" in q or "culture" in q:
        extra_terms += ["personality", "behavioral"]

    return query + " " + " ".join(set(extra_terms))
