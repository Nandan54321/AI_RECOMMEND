def rule_score(query: str, skills: list):
    score = 0

    for skill in skills:
        if skill.lower() in query.lower():
            score += 10

    return min(score, 100)