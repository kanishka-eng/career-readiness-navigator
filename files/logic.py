"""
logic.py
Skill-gap calculation + gamification helpers (levels, XP, badges).
Swap calculate_gap()/build_roadmap() for a more advanced algorithm later —
keep the same return shapes and the UI keeps working.
"""

from career_data import RESOURCES, MAX_LEVEL

LEVELS = [
    (0, "🌱 Rookie"),
    (25, "🚀 Explorer"),
    (50, "⚡ Achiever"),
    (75, "🔥 Pro"),
    (95, "👑 Job-Ready Legend"),
]

BADGE_DEFS = [
    ("first_skill", "🧩", "First Steps", "Select your first skill"),
    ("career_locked", "🎯", "Target Locked", "Choose a career"),
    ("halfway", "⚡", "Halfway There", "Reach 50% readiness"),
    ("first_gap_closed", "✅", "Gap Closer", "Complete your first roadmap item"),
    ("job_ready", "👑", "Job Ready", "Reach 80% combined readiness"),
    ("perfectionist", "💯", "Perfectionist", "Close every skill gap"),
]


def calculate_gap(current_skills: set, required_skills: dict) -> dict:
    """
    current_skills: set of skill names the student has
    required_skills: {skill: required_level 1-5} for the chosen career
    """
    matched = {s: w for s, w in required_skills.items() if s in current_skills}
    gap = {s: w for s, w in required_skills.items() if s not in current_skills}

    total_weight = sum(required_skills.values()) or 1
    matched_weight = sum(matched.values())
    readiness = round((matched_weight / total_weight) * 100, 1)

    return {"matched": matched, "gap": gap, "readiness": readiness}


def build_roadmap(gap: dict) -> list:
    """Highest required-level skills first."""
    ordered = sorted(gap.items(), key=lambda kv: kv[1], reverse=True)
    return [{"skill": s, "level": lvl, "resources": RESOURCES.get(s, [])} for s, lvl in ordered]


def get_level(combined_score: float) -> tuple:
    """Returns (label, next_threshold) for a 0-100 combined score."""
    current = LEVELS[0][1]
    next_threshold = 100
    for i, (thresh, label) in enumerate(LEVELS):
        if combined_score >= thresh:
            current = label
            next_threshold = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else 100
    return current, next_threshold


def compute_badges(state: dict) -> set:
    """
    state: {
        skills_selected: int, career_chosen: bool,
        readiness: float, roadmap_items_done: int,
        gap_remaining: int, combined_score: float,
    }
    Returns the set of badge ids that should be unlocked.
    """
    unlocked = set()
    if state.get("skills_selected", 0) >= 1:
        unlocked.add("first_skill")
    if state.get("career_chosen"):
        unlocked.add("career_locked")
    if state.get("readiness", 0) >= 50:
        unlocked.add("halfway")
    if state.get("roadmap_items_done", 0) >= 1:
        unlocked.add("first_gap_closed")
    if state.get("combined_score", 0) >= 80:
        unlocked.add("job_ready")
    if state.get("career_chosen") and state.get("gap_remaining", 1) == 0:
        unlocked.add("perfectionist")
    return unlocked
