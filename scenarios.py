"""Fixed scenarios for the five criteria in criteria.md."""

MATCHING_QUERIES = [
    "Levi's 501 jeans",
    "butterfly baby tee",
    "oversized flannel plaid",
    "90s track jacket navy stripe",
    "silk slip dress floral midi",
]

CRITERIA = {
    1: ("A matching query completes all three tools", "4 of 5"),
    2: ("An impossible query stops before the second tool", "5 of 5"),
    3: ("The selected item stays the same between tools", "5 of 5"),
    4: ("The fit card includes the find's details in a short caption", "4 of 5"),
    5: ("Search respects the user's price ceiling", "5 of 5"),
}

SCENARIOS = [
    {"name": "matching query completes", "query": "vintage graphic tee under $30",
     "wardrobe": "example", "criterion": 1},
    {"name": "impossible query stops early", "query": "spacesuit size XXS under $1",
     "wardrobe": "example", "criterion": 2},
    *[
        {"name": f"criterion {criterion}: {query}", "query": query,
         "wardrobe": "example", "criterion": criterion}
        for criterion in (3, 4)
        for query in MATCHING_QUERIES
    ],
    {"name": "inclusive price ceiling", "query": "graphic tee under $18",
     "wardrobe": "example", "criterion": 5},
]


def validate() -> list[str]:
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in ("example", "empty"):
            problems.append(f"scenario {i} has an invalid wardrobe")
        if scenario.get("criterion") not in CRITERIA:
            problems.append(f"scenario {i} has an invalid criterion")
    if {s.get("criterion") for s in SCENARIOS} != set(CRITERIA):
        problems.append("Scenarios must cover all five criteria")
    return problems
