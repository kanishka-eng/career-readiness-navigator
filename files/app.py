"""
app.py — Career Readiness Navigator (Gamified Edition)
Run with:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go

from career_data import CAREERS, SKILL_CATEGORIES, MAX_LEVEL
from logic import calculate_gap, build_roadmap, get_level, compute_badges, BADGE_DEFS

st.set_page_config(page_title="Career Readiness Navigator", page_icon="🎯", layout="wide")

# ----------------------------------------------------------------------
# STYLE — glassmorphism, glow, motion. This is the "dashing" part.
# ----------------------------------------------------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
h1, h2, h3, .glow-title { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: radial-gradient(circle at 15% 10%, #1b1035 0%, #0d0b1f 45%, #070611 100%);
    background-attachment: fixed;
}

@keyframes floatGlow {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-6px); }
    100% { transform: translateY(0px); }
}
@keyframes popIn {
    0%   { opacity: 0; transform: scale(0.85); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes shimmer {
    0%   { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

.hero {
    text-align: center;
    padding: 34px 10px 18px 10px;
    animation: popIn 0.5s ease;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #8A6CFF, #4FD8EA, #8A6CFF);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
    margin-bottom: 4px;
}
.hero p { color: #a9a3c9; font-size: 1.05rem; }

/* HUD strip */
.hud {
    display: flex;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
    margin-bottom: 6px;
    animation: popIn 0.6s ease;
}
.hud-chip {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(6px);
    border-radius: 999px;
    padding: 8px 18px;
    font-size: 0.9rem;
    font-weight: 600;
    color: #e8e6ff;
    animation: floatGlow 3.5s ease-in-out infinite;
}

/* skill chips */
div.stButton > button {
    border-radius: 999px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    background: rgba(255,255,255,0.04) !important;
    color: #e8e6ff !important;
    font-weight: 600 !important;
    transition: all 0.18s ease !important;
    animation: popIn 0.35s ease;
}
div.stButton > button:hover {
    border-color: #8A6CFF !important;
    background: rgba(138,108,255,0.18) !important;
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 6px 18px rgba(138,108,255,0.35);
}

/* career cards */
.career-card {
    border-radius: 20px;
    padding: 22px 16px;
    text-align: center;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
    animation: popIn 0.4s ease;
}
.career-card:hover { transform: translateY(-5px); border-color: #4FD8EA; }
.career-card-selected {
    border-radius: 20px;
    padding: 22px 16px;
    text-align: center;
    background: linear-gradient(160deg, rgba(138,108,255,0.28), rgba(79,216,234,0.18));
    border: 1.5px solid #4FD8EA;
    box-shadow: 0 0 26px rgba(79,216,234,0.35);
    animation: popIn 0.4s ease;
}
.career-icon { font-size: 2.4rem; }
.career-name { font-weight: 700; font-size: 1.05rem; margin: 6px 0 2px 0; color: #fff; }
.career-tag { font-size: 0.8rem; color: #a9a3c9; }

/* tags */
.gap-tag {
    display: inline-block; padding: 6px 14px; margin: 4px;
    border-radius: 999px; font-size: 0.85rem; font-weight: 600;
    animation: popIn 0.3s ease;
}
.gap-missing { background: rgba(255,90,110,0.16); color: #ff6b81; border: 1px solid rgba(255,107,129,0.35); }
.gap-matched { background: rgba(79,216,234,0.16); color: #4FD8EA; border: 1px solid rgba(79,216,234,0.35); }

/* badges */
.badge {
    display: inline-block; width: 96px; text-align: center;
    margin: 8px; padding: 14px 6px; border-radius: 16px;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    transition: all 0.2s ease;
}
.badge-unlocked { border-color: #FFD166; box-shadow: 0 0 18px rgba(255,209,102,0.35); animation: popIn 0.4s ease; }
.badge-icon { font-size: 1.8rem; }
.badge-locked { opacity: 0.28; filter: grayscale(1); }
.badge-name { font-size: 0.7rem; margin-top: 4px; color: #cfcaea; }

/* section headers */
.section-title { font-weight: 700; font-size: 1.35rem; color: #fff; margin-bottom: 2px; }
.section-sub { color: #a9a3c9; font-size: 0.9rem; margin-bottom: 14px; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------
defaults = {
    "selected_skills": set(),
    "selected_career": None,
    "completed_roadmap_items": set(),
    "unlocked_badges": set(),
    "last_level": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def sync_gamification():
    """Recompute readiness / badges / level, fire toasts + confetti on new unlocks."""
    career = st.session_state.selected_career
    skills = st.session_state.selected_skills
    readiness, gap_count, roadmap_len = 0, 0, 0

    if career:
        required = CAREERS[career]["skills"]
        result = calculate_gap(skills, required)
        readiness = result["readiness"]
        gap_count = len(result["gap"])
        roadmap_len = len(required)

    done = sum(1 for k in st.session_state.completed_roadmap_items if k.startswith(f"{career}::")) if career else 0
    roadmap_pct = round((done / (gap_count + done)) * 100, 1) if (gap_count + done) else (100.0 if career else 0.0)
    combined = round((readiness + roadmap_pct) / 2, 1) if career else 0.0

    state = {
        "skills_selected": len(skills),
        "career_chosen": bool(career),
        "readiness": readiness,
        "roadmap_items_done": done,
        "gap_remaining": gap_count,
        "combined_score": combined,
    }
    newly_unlocked = compute_badges(state) - st.session_state.unlocked_badges
    for bid in newly_unlocked:
        name = next(b[2] for b in BADGE_DEFS if b[0] == bid)
        st.toast(f"🏅 Badge unlocked: {name}!")
    st.session_state.unlocked_badges |= newly_unlocked

    level_label, _ = get_level(combined)
    if st.session_state.last_level and level_label != st.session_state.last_level:
        st.balloons()
    st.session_state.last_level = level_label

    return readiness, combined, level_label


readiness_now, combined_now, level_now = sync_gamification()
xp = int(combined_now * 10)

# ----------------------------------------------------------------------
# HERO + HUD
# ----------------------------------------------------------------------
st.markdown(f"""
<div class="hero">
    <h1>🎯 Career Readiness Navigator</h1>
    <p>Level up from student to job-ready — one skill at a time.</p>
</div>
<div class="hud">
    <div class="hud-chip">🏆 {level_now}</div>
    <div class="hud-chip">⚡ {xp} XP</div>
    <div class="hud-chip">🧩 {len(st.session_state.selected_skills)} skills selected</div>
    <div class="hud-chip">🎖️ {len(st.session_state.unlocked_badges)}/{len(BADGE_DEFS)} badges</div>
</div>
""", unsafe_allow_html=True)
st.write("")

# ----------------------------------------------------------------------
# TABS
# ----------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧑‍💻  Your Skills", "🎯  Choose Career", "📊  Skill Gap", "🗺️  Roadmap", "🏆  Progress & Badges",
])

# TAB 1 — SKILLS
with tab1:
    st.markdown('<div class="section-title">What skills do you already have?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Tap a skill to toggle it. Each pick earns XP instantly.</div>', unsafe_allow_html=True)

    for category, skills in SKILL_CATEGORIES.items():
        st.markdown(f"**{category}**")
        cols = st.columns(4)
        for i, skill in enumerate(skills):
            selected = skill in st.session_state.selected_skills
            label = f"✅ {skill}" if selected else skill
            if cols[i % 4].button(label, key=f"chip_{skill}", use_container_width=True):
                if selected:
                    st.session_state.selected_skills.discard(skill)
                else:
                    st.session_state.selected_skills.add(skill)
                    st.toast(f"+10 XP — {skill} added!")
                st.rerun()
        st.write("")

    if not st.session_state.selected_skills:
        st.info("Select a few skills, then head to **Choose Career**. 🎯")

# TAB 2 — CAREER
with tab2:
    st.markdown('<div class="section-title">Pick the career you\'re aiming for</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Your roadmap and gap analysis are built around this choice.</div>', unsafe_allow_html=True)

    cols = st.columns(len(CAREERS))
    for i, (career, info) in enumerate(CAREERS.items()):
        with cols[i]:
            is_selected = st.session_state.selected_career == career
            card_class = "career-card-selected" if is_selected else "career-card"
            st.markdown(
                f"""<div class="{card_class}">
                        <div class="career-icon">{info['icon']}</div>
                        <div class="career-name">{career}</div>
                        <div class="career-tag">{info['tagline']}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
            btn_label = "✅ Locked In" if is_selected else "Select"
            if st.button(btn_label, key=f"career_{career}", use_container_width=True):
                first_pick = st.session_state.selected_career is None
                st.session_state.selected_career = career
                if first_pick:
                    st.toast(f"🎯 Target locked: {career}!")
                st.rerun()

# TAB 3 — GAP
with tab3:
    career = st.session_state.selected_career
    skills = st.session_state.selected_skills

    if not career:
        st.warning("Choose a career in the **Choose Career** tab first.")
    elif not skills:
        st.warning("Select your current skills in the **Your Skills** tab first.")
    else:
        required = CAREERS[career]["skills"]
        result = calculate_gap(skills, required)

        c1, c2 = st.columns([1, 1.2])
        with c1:
            st.markdown(f'<div class="section-title">Readiness for {career}</div>', unsafe_allow_html=True)
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=result["readiness"],
                number={"suffix": "%", "font": {"size": 44, "color": "#fff"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#8884"},
                    "bar": {"color": "#4FD8EA"},
                    "bgcolor": "rgba(255,255,255,0.04)",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 50], "color": "rgba(255,107,129,0.25)"},
                        {"range": [50, 80], "color": "rgba(255,209,102,0.25)"},
                        {"range": [80, 100], "color": "rgba(79,216,234,0.25)"},
                    ],
                },
            ))
            fig.update_layout(height=280, margin=dict(l=20, r=20, t=10, b=10),
                               paper_bgcolor="rgba(0,0,0,0)", font={"color": "#fff"})
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**✅ Skills you have**")
            st.markdown(
                "".join(f'<span class="gap-tag gap-matched">{s}</span>' for s in result["matched"]) or "<span style='color:#888'>None yet.</span>",
                unsafe_allow_html=True,
            )
            st.markdown("**❌ Skill gaps**")
            st.markdown(
                "".join(f'<span class="gap-tag gap-missing">{s}</span>' for s in result["gap"]) or "<span style='color:#888'>No gaps — fully covered! 🎉</span>",
                unsafe_allow_html=True,
            )

        with c2:
            skill_names = list(required.keys())
            required_vals = [required[s] for s in skill_names]
            current_vals = [required[s] if s in skills else 0 for s in skill_names]
            fig2 = go.Figure()
            fig2.add_trace(go.Scatterpolar(r=required_vals, theta=skill_names, fill='toself',
                                            name='Required', line_color='#8A6CFF', opacity=0.55))
            fig2.add_trace(go.Scatterpolar(r=current_vals, theta=skill_names, fill='toself',
                                            name='You', line_color='#4FD8EA', opacity=0.75))
            fig2.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, MAX_LEVEL], color="#a9a3c9"),
                           bgcolor="rgba(0,0,0,0)", angularaxis=dict(color="#e8e6ff")),
                showlegend=True, height=460, margin=dict(l=30, r=30, t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)", font={"color": "#e8e6ff"},
                legend=dict(font=dict(color="#e8e6ff")),
            )
            st.plotly_chart(fig2, use_container_width=True)

# TAB 4 — ROADMAP
with tab4:
    career = st.session_state.selected_career
    skills = st.session_state.selected_skills

    if not career or not skills:
        st.warning("Complete the **Your Skills** and **Choose Career** tabs first.")
    else:
        required = CAREERS[career]["skills"]
        result = calculate_gap(skills, required)
        roadmap = build_roadmap(result["gap"])

        st.markdown(f'<div class="section-title">Your roadmap → {career}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Ordered by importance. Check items off — XP and badges update live.</div>', unsafe_allow_html=True)

        if not roadmap:
            st.success("No gaps left to close — you're ready! 🎉")
            st.balloons()
        else:
            for idx, item in enumerate(roadmap, start=1):
                item_key = f"{career}::{item['skill']}"
                done = item_key in st.session_state.completed_roadmap_items
                with st.expander(f"{'✅' if done else '⬜'} Step {idx}: {item['skill']}  ·  Required level {item['level']}/5", expanded=not done):
                    checked = st.checkbox("Mark as completed", value=done, key=f"chk_{item_key}")
                    if checked and not done:
                        st.session_state.completed_roadmap_items.add(item_key)
                        st.toast(f"🎉 +50 XP — {item['skill']} closed!")
                        st.rerun()
                    elif not checked and done:
                        st.session_state.completed_roadmap_items.discard(item_key)
                        st.rerun()
                    if item["resources"]:
                        st.markdown("**Resources:**")
                        for name, url in item["resources"]:
                            st.markdown(f"- [{name}]({url})")

# TAB 5 — PROGRESS & BADGES
with tab5:
    career = st.session_state.selected_career
    skills = st.session_state.selected_skills

    st.markdown('<div class="section-title">Badge shelf</div>', unsafe_allow_html=True)
    badge_html = ""
    for bid, icon, name, desc in BADGE_DEFS:
        unlocked = bid in st.session_state.unlocked_badges
        cls = "badge badge-unlocked" if unlocked else "badge badge-locked"
        badge_html += f"""<div class="{cls}" title="{desc}">
                              <div class="badge-icon">{icon}</div>
                              <div class="badge-name">{name}</div>
                           </div>"""
    st.markdown(f'<div style="display:flex; flex-wrap:wrap;">{badge_html}</div>', unsafe_allow_html=True)
    st.write("")

    if not career or not skills:
        st.warning("Complete the earlier tabs to see your full progress.")
    else:
        required = CAREERS[career]["skills"]
        result = calculate_gap(skills, required)
        roadmap = build_roadmap(result["gap"])
        total_steps = len(roadmap) + len(result["matched"])
        done_steps = sum(1 for item in roadmap if f"{career}::{item['skill']}" in st.session_state.completed_roadmap_items) + len(result["matched"])
        roadmap_pct = round((done_steps / total_steps) * 100, 1) if total_steps else 100.0
        combined = round((result["readiness"] + roadmap_pct) / 2, 1)
        level_label, next_threshold = get_level(combined)

        st.markdown('<div class="section-title">Your stats</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Skill readiness", f"{result['readiness']}%")
        c2.metric("Roadmap progress", f"{roadmap_pct}%")
        c3.metric("Combined score", f"{combined}%")
        c4.metric("Level", level_label)

        st.progress(min(combined / 100, 1.0))
        st.caption(f"XP: {int(combined*10)} — next level at {next_threshold}% combined score")

        if combined >= 80:
            st.success("You're in great shape for this role — recruiters would like this profile. 🚀")
        elif combined >= 50:
            st.info("Solid progress. Keep closing roadmap items to level up. 💪")
        else:
            st.warning("Just getting started — follow the roadmap step by step. 🌱")
