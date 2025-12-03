from __future__ import annotations
import streamlit as st
import os
from ui_theme import inject_theme, render_hero, success_confetti, section_title, render_divider
try:
    from ui_theme_alt import inject_theme_alt, render_hero_alt, section_title_alt, render_divider_alt
    ALT_THEME_AVAILABLE = True
except Exception:
    ALT_THEME_AVAILABLE = False

# Compatibility imports for AG2/AutoGen swarm APIs
try:
    # Preferred AG2/AutoGen agentchat namespace (newer versions)
    from autogen.agentchat import (
        SwarmAgent,
        SwarmResult,
        initiate_swarm_chat,
        OpenAIWrapper,
        AFTER_WORK,
        UPDATE_SYSTEM_MESSAGE,
    )
except ImportError:
    try:
        # Fallback to legacy autogen namespace (older versions)
        from autogen import (
            SwarmAgent,
            SwarmResult,
            initiate_swarm_chat,
            OpenAIWrapper,
            AFTER_WORK,
            UPDATE_SYSTEM_MESSAGE,
        )
    except ImportError as e:
        SwarmAgent = None
        # Provide a minimal placeholder so type annotations don't fail
        class _FallbackSwarmResult:
            def __init__(self, agent: str, context_variables: dict):
                self.agent = agent
                self.context_variables = context_variables

        SwarmResult = _FallbackSwarmResult  # type: ignore
        try:
            from openai import OpenAI
        except Exception:
            OpenAI = None


os.environ["AUTOGEN_USE_DOCKER"] = "0"

if 'output' not in st.session_state:
    st.session_state.output = {
        'assessment': '',
        'action': '',
        'followup': ''
    }

# Sidebar logo at the very top (above API Key section)
try:
    st.sidebar.image("logo.png", use_container_width=True)
except Exception:
    import os
    here = os.path.dirname(__file__)
    logo_path = os.path.join(here, "logo.png")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)

st.sidebar.title("OpenAI API Key")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Optional: choose model when using OpenAI fallback or to pass into AG2 config
model_choice = st.sidebar.selectbox(
    "Model",
    ["gpt-4.1-nano", "gpt-4o-mini", "gpt-5-nano"],
    index=0,
)

# Sidebar theme switcher
st.sidebar.markdown("### Theme")
theme_options = ["Default"] + (["Neon Pulse"] if ALT_THEME_AVAILABLE else [])
selected_theme = st.sidebar.selectbox("UI Theme", theme_options, index=0, key="theme_select")

# Sidebar accent color pickers (override theme CSS vars)
st.sidebar.markdown("### Accents")
primary_accent = st.sidebar.color_picker("Primary", value="#22c55e", key="accent_primary")
secondary_accent = st.sidebar.color_picker("Secondary", value="#10b981", key="accent_secondary")

# Sidebar demo controls applied BEFORE widgets render
st.sidebar.subheader("Quick Demo")
prefill_clicked = st.sidebar.button("Prefill demo inputs", key="btn_demo_prefill")
st.sidebar.subheader("Auto Suggest")
auto_on = st.sidebar.checkbox(
    "Auto-fill all sections (demo)",
    value=st.session_state.get("auto_suggest", False),
    key="auto_suggest",
)

if prefill_clicked:
    st.session_state['mental_state'] = "Feeling overwhelmed lately, sleep is irregular, anxious about work."
    st.session_state['recent_changes'] = "Changed jobs last month; moved to a new city."
    st.session_state['support_system'] = ["Friends"]
    st.session_state['current_symptoms'] = ["Anxiety", "Insomnia", "Fatigue"]
    st.session_state['stress_level'] = 7
    st.session_state['sleep_pattern'] = "6"
    st.rerun()

if st.session_state.get("auto_suggest"):
    if not st.session_state.get("_auto_applied", False):
        # Screeners
        for i in range(9):
            st.session_state[f"phq_{i}"] = "1 - Several days" if i < 7 else ("2 - More than half the days" if i == 7 else "0 - Not at all")
        for i in range(7):
            st.session_state[f"gad_{i}"] = "1 - Several days" if i < 5 else "2 - More than half the days"
        # Coping toolkit demo notes
        st.session_state['grounding_demo'] = {
            'sees': 'Window, mug, book, plant, pen',
            'feels': 'Feet on floor, chair, shirt, air',
            'hears': 'Fan, distant traffic, typing',
            'smells': 'Coffee, soap',
            'tastes': 'Mint',
        }
        # Resource filters demo
        st.session_state['city'] = st.session_state.get('city', '') or "Delhi"
        # Care path suggestion
        st.session_state['care_path_autosuggest'] = {'duration': '3 weeks', 'focus': 'Anxiety management'}
        # Apply care path widget values before widgets render
        st.session_state['path_len'] = st.session_state['care_path_autosuggest']['duration']
        st.session_state['focus'] = st.session_state['care_path_autosuggest']['focus']
        # Playlist demo
        if 'playlists' not in st.session_state or not st.session_state['playlists']:
            st.session_state['playlists'] = [{
                'name': 'Quick Relief',
                'steps': ["Box Breathing (4 cycles)", "Grounding (5-4-3-2-1)", "Journaling (2 min)"]
            }]
        # Check-in demo
        if 'checkins' not in st.session_state or not st.session_state['checkins']:
            st.session_state['checkins'] = [{"mood": 5, "sleep": 6, "stress": 7}]
        st.session_state["_auto_applied"] = True
        st.rerun()
else:
    st.session_state["_auto_applied"] = False

# Sidebar developer footer (placed near bottom of sidebar)
st.sidebar.markdown("---")
st.sidebar.markdown("#### Developer")
try:
    st.sidebar.image("developer.jpg", caption="Abhishek Kumar", use_container_width=True)
except Exception:
    try:
        import os
        here = os.path.dirname(__file__)
        dev_path = os.path.join(here, "developer.jpg")
        if os.path.exists(dev_path):
            st.sidebar.image(dev_path, caption="Abhishek Kumar", use_container_width=True)
    except Exception:
        st.sidebar.caption("Abhishek Kumar")

if selected_theme == "Neon Pulse" and ALT_THEME_AVAILABLE:
    inject_theme_alt()
    render_hero_alt()
    section_title_fn = section_title_alt
    divider_fn = render_divider_alt
else:
    inject_theme()
    render_hero()
    section_title_fn = section_title
    divider_fn = render_divider

# Apply accent overrides to CSS variables
if selected_theme == "Neon Pulse" and ALT_THEME_AVAILABLE:
    st.markdown(f"<style>:root{{--cyan:{primary_accent};--magenta:{secondary_accent};}}</style>", unsafe_allow_html=True)
else:
    st.markdown(f"<style>:root{{--primary:{primary_accent};--primary-2:{secondary_accent};--accent:{primary_accent};--accent-2:{secondary_accent};}}</style>", unsafe_allow_html=True)

# Agent Team Showcase (interactive)
st.markdown("""
<div class="agent-grid">
    <div class="agent-card">
        <div class="agent-emoji">🧠</div>
        <div class="agent-title">Assessment</div>
        <div class="agent-sub">Understand your state with empathy and clarity.</div>
    </div>
    <div class="agent-card">
        <div class="agent-emoji">🎯</div>
        <div class="agent-title">Action</div>
        <div class="agent-sub">Immediate steps, tools, and right-fit resources.</div>
    </div>
    <div class="agent-card">
        <div class="agent-emoji">🔄</div>
        <div class="agent-title">Follow‑up</div>
        <div class="agent-sub">Care pathways and gentle long‑term momentum.</div>
    </div>
</div>
""", unsafe_allow_html=True)

ag_col1, ag_col2, ag_col3 = st.columns(3)
with ag_col1:
        if st.button("Assess me", key="btn_assess_me"):
                st.session_state["expand_phq"], st.session_state["expand_gad"] = True, True
                st.rerun()
with ag_col2:
        if st.button("Guide me now", key="btn_action_now"):
                st.session_state["triage_action"] = "grounding"
                st.session_state["highlight_coping"] = True
                st.rerun()
with ag_col3:
        if st.button("Build my path", key="btn_build_path"):
                st.session_state["highlight_care_path"] = True
                st.rerun()

section_title_fn("Personal Information", "👤")
col1, col2 = st.columns(2)

with col1:
    mental_state = st.text_area(
        "How have you been feeling recently?",
        placeholder="Describe your emotional state, thoughts, or concerns...",
        key="mental_state",
    )
    sleep_pattern = st.select_slider(
        "Sleep Pattern (hours per night)",
        options=[f"{i}" for i in range(0, 13)],
        value="7",
        key="sleep_pattern",
    )
    
with col2:
    stress_level = st.slider("Current Stress Level (1-10)", 1, 10, 5, key="stress_level")
    support_system = st.multiselect(
        "Current Support System",
        ["Family", "Friends", "Therapist", "Support Groups", "None"],
        default=st.session_state.get("support_system", []),
        key="support_system",
    )

recent_changes = st.text_area(
    "Any significant life changes or events recently?",
    placeholder="Job changes, relationships, losses, etc...",
    key="recent_changes",
)

current_symptoms = st.multiselect(
    "Current Symptoms",
    ["Anxiety", "Depression", "Insomnia", "Fatigue", "Loss of Interest", 
     "Difficulty Concentrating", "Changes in Appetite", "Social Withdrawal",
     "Mood Swings", "Physical Discomfort"],
    default=st.session_state.get("current_symptoms", []),
    key="current_symptoms",
)

# (Old) demo/auto-suggest section removed; handled at top before widgets

divider_fn()
section_title_fn("Triage Assistant", "🛡️")

def detect_crisis(text: str) -> bool:
    if not text:
        return False
    keywords = [
        "suicide", "hurt myself", "end it", "kill myself",
        "self-harm", "can't go on", "hopeless",
    ]
    t = text.lower()
    return any(k in t for k in keywords)

# Try to reuse PHQ/GAD totals from widgets
try:
    triage_phq = sum(int(st.session_state.get(f"phq_{i}", "0 - Not at all").split(" ")[0]) for i in range(9))
    triage_gad = sum(int(st.session_state.get(f"gad_{i}", "0 - Not at all").split(" ")[0]) for i in range(7))
except Exception:
    triage_phq, triage_gad = 0, 0

sleep_hours = int(str(sleep_pattern)) if str(sleep_pattern).isdigit() else 7
flags = []
if triage_phq >= 15:
    flags.append("High depression indicators (PHQ-9 ≥15)")
if triage_gad >= 15:
    flags.append("High anxiety indicators (GAD-7 ≥15)")
if stress_level >= 8:
    flags.append("High current stress (≥8)")
if sleep_hours <= 5:
    flags.append("Insufficient sleep (≤5h)")
if detect_crisis(mental_state) or detect_crisis(recent_changes):
    flags.append("Crisis language detected — prioritize immediate help")

def severity_badge():
    level = "info"
    if any("Crisis" in f for f in flags):
        level = "high"
    elif triage_phq >= 15 or triage_gad >= 15 or stress_level >= 8:
        level = "moderate"
    return level

sense = st.select_slider("Sensitivity", options=["Conservative", "Standard", "Proactive"], value="Standard")
if sense == "Conservative":
    flags = [f for f in flags if ("High" in f or "Crisis" in f)]
elif sense == "Proactive":
    # keep all flags, including sleep
    flags = flags

if flags:
    sev = severity_badge()
    if sev == "high":
        st.error("High-risk: " + "; ".join(flags))
    elif sev == "moderate":
        st.warning("Moderate-risk: " + "; ".join(flags))
    else:
        st.info("Info: " + "; ".join(flags))

    # Inline grounding quick start
    with st.container():
        gcol1, gcol2, gcol3, gcol4 = st.columns(4)
        with gcol1:
            if st.button("Start Grounding"):
                st.session_state['triage_action'] = "grounding"
        with gcol2:
            if st.button("View Resources"):
                st.session_state['triage_action'] = "resources"
        with gcol3:
            if st.button("Crisis Support"):
                st.session_state['triage_action'] = "crisis"
        with gcol4:
            msg = "Hello, I'm seeking support for stress/anxiety. Do you have low-cost/insurance and remote options?"
            st.download_button("Copy Outreach Message", msg, file_name="outreach.txt", mime="text/plain")

    act = st.session_state.get('triage_action')
    if act == "grounding":
        st.info("Try 5-4-3-2-1 grounding and 4x box breathing.")
        # Minimal inline grounding guide
        st.markdown("- See 5, Feel 4, Hear 3, Smell 2, Taste 1")
    elif act == "resources":
        st.info("Scroll to 'Find Support Resources' and search with broader filters or remote options.")
    elif act == "crisis":
        st.error("If you are in crisis: Call 988 (US) or local emergency services (112/999). Seek immediate professional help.")
    st.caption("Privacy: No data leaves your device unless you choose to send.")

divider_fn()
section_title_fn("Screening (Optional)", "🧪")
with st.expander("PHQ-9 Depression Screener", expanded=st.session_state.get("expand_phq", False)):
    phq_questions = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
        "Trouble concentrating on things, such as reading or watching television",
        "Moving or speaking so slowly that other people could have noticed. Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead, or of hurting yourself in some way",
    ]
    phq_scale = ["0 - Not at all", "1 - Several days", "2 - More than half the days", "3 - Nearly every day"]
    phq_scores = []
    for i, q in enumerate(phq_questions):
        sel = st.selectbox(q, phq_scale, key=f"phq_{i}")
        phq_scores.append(int(sel.split(" ")[0]))
    phq_total = sum(phq_scores)
    st.write(f"PHQ-9 Total Score: {phq_total}")
    phq_level = (
        "Minimal (0–4)" if phq_total <= 4 else
        "Mild (5–9)" if phq_total <= 9 else
        "Moderate (10–14)" if phq_total <= 14 else
        "Moderately severe (15–19)" if phq_total <= 19 else
        "Severe (20–27)"
    )
    st.info(f"Severity: {phq_level}")

with st.expander("GAD-7 Anxiety Screener", expanded=st.session_state.get("expand_gad", False)):
    gad_questions = [
        "Feeling nervous, anxious, or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid, as if something awful might happen",
    ]
    gad_scale = ["0 - Not at all", "1 - Several days", "2 - More than half the days", "3 - Nearly every day"]
    gad_scores = []
    for i, q in enumerate(gad_questions):
        sel = st.selectbox(q, gad_scale, key=f"gad_{i}")
        gad_scores.append(int(sel.split(" ")[0]))
    gad_total = sum(gad_scores)
    st.write(f"GAD-7 Total Score: {gad_total}")
    gad_level = (
        "Minimal (0–4)" if gad_total <= 4 else
        "Mild (5–9)" if gad_total <= 9 else
        "Moderate (10–14)" if gad_total <= 14 else
        "Severe (15–21)"
    )
    st.info(f"Severity: {gad_level}")

divider_fn()
section_title_fn("Coping Toolkit", "🧰")
if st.session_state.get("highlight_coping"):
    st.info("Jumped here from Agent actions — try Box Breathing or Grounding.")
    st.session_state["highlight_coping"] = False
coping_tab1, coping_tab2, coping_tab3 = st.tabs(["Box Breathing", "Grounding 5-4-3-2-1", "Journaling Prompts"])
with coping_tab1:
    st.write("Follow a 4-4-4-4 pattern: inhale, hold, exhale, hold.")
    dur = st.slider("Cycle seconds", 3, 6, 4)
    cycles = st.slider("Cycles", 1, 10, 4)
    if st.button("Start Breathing Timer"):
        import time
        ph = st.empty()
        for c in range(cycles):
            for phase in ["Inhale", "Hold", "Exhale", "Hold"]:
                ph.markdown(f"**{phase}** for {dur}s")
                time.sleep(dur)
        ph.markdown("Session complete. Notice how you feel.")
with coping_tab2:
    st.write("Name 5 things you can see, 4 you can feel, 3 you can hear, 2 you can smell, 1 you can taste.")
    demo = st.session_state.get('grounding_demo') or {}
    sees = st.text_area("5 things you see", demo.get('sees', ''), key="grounding_sees")
    feels = st.text_area("4 things you feel", demo.get('feels', ''), key="grounding_feels")
    hears = st.text_area("3 things you hear", demo.get('hears', ''), key="grounding_hears")
    smells = st.text_area("2 things you smell", demo.get('smells', ''), key="grounding_smells")
    tastes = st.text_area("1 thing you taste", demo.get('tastes', ''), key="grounding_tastes")
    if st.button("Save Grounding Notes"):
        st.success("Saved. Revisit what helped the most.")
with coping_tab3:
    st.write("Pick a prompt to journal for 5 minutes.")
    prompt = st.selectbox("Prompt", [
        "What felt heavy today, and what eased it?",
        "If a friend felt like you, what would you tell them?",
        "List three small wins from the past week.",
        "What support sounds helpful right now?",
    ])
    entry = st.text_area("Your journal entry")
    if st.button("Save Journal Entry"):
        st.success("Entry saved locally for this session.")

divider_fn()
section_title_fn("Session Playlists", "🎵")
if 'playlists' not in st.session_state:
    st.session_state['playlists'] = []
if 'favorite_playlists' not in st.session_state:
    st.session_state['favorite_playlists'] = set()
playlist_steps = st.multiselect(
    "Build a short session",
    ["Box Breathing (4 cycles)", "Grounding (5-4-3-2-1)", "Journaling (2 min)", "Micro-walk (3 min)"],
)
pl_name = st.text_input("Playlist name", "My Session")
if st.button("Save Playlist") and playlist_steps:
    st.session_state['playlists'].append({"name": pl_name, "steps": playlist_steps})
    st.success("Playlist saved.")

# Favorite toggle
fav_pl = st.selectbox("Favorite a playlist", [p["name"] for p in st.session_state['playlists']] if st.session_state['playlists'] else ["None"], index=0)
if st.button("Toggle Favorite") and st.session_state['playlists']:
    if fav_pl in st.session_state['favorite_playlists']:
        st.session_state['favorite_playlists'].remove(fav_pl)
    else:
        st.session_state['favorite_playlists'].add(fav_pl)
    st.info(f"Favorites: {', '.join(st.session_state['favorite_playlists']) if st.session_state['favorite_playlists'] else 'None'}")

def run_step(step: str):
    import time
    ph = st.empty()
    if step.startswith("Box Breathing"):
        total = 16
        for phase in ["Inhale", "Hold", "Exhale", "Hold"]:
            ph.markdown(f"**{phase}** — 4s")
            # countdown with pause/skip controls
            pause_key = f"pause_{phase}"
            skip_key = f"skip_{phase}"
            st.session_state.setdefault(pause_key, False)
            st.session_state.setdefault(skip_key, False)
            for i in range(4, 0, -1):
                ph.markdown(f"{phase}: {i}s")
                if st.button("Pause", key=pause_key):
                    time.sleep(1)
                if st.button("Skip", key=skip_key):
                    break
                time.sleep(1)
    elif step.startswith("Grounding"):
        ph.markdown("Name 5 see, 4 feel, 3 hear, 2 smell, 1 taste.")
        # short countdown
        for i in range(5, 0, -1):
            ph.markdown(f"Grounding: {i}s")
            time.sleep(1)
    elif step.startswith("Journaling"):
        ph.markdown("Write two sentences about what you feel and one helpful action.")
        for i in range(10, 0, -1):
            ph.markdown(f"Journaling: {i}s")
            time.sleep(1)
    elif step.startswith("Micro-walk"):
        ph.markdown("Walk around for 3 minutes or stretch gently.")
        for i in range(10, 0, -1):
            ph.markdown(f"Movement: {i}s")
            time.sleep(1)
    ph.markdown("Step complete.")

selected_pl = st.selectbox("Run playlist", [p["name"] for p in st.session_state['playlists']] if st.session_state['playlists'] else ["None"], index=0)
if st.button("Start Session") and st.session_state['playlists']:
    pl = next((p for p in st.session_state['playlists'] if p["name"] == selected_pl), None)
    if pl:
        relief_scores = []
        for s in pl["steps"]:
            st.markdown(f"### {s}")
            run_step(s)
            relief = st.slider("Relief after this step (0–10)", 0, 10, 5, key=f"relief_{s}")
            relief_scores.append(relief)
        avg_relief = sum(relief_scores) / len(relief_scores) if relief_scores else 0
        st.success(f"Session done. Average relief: {avg_relief:.1f}/10")
        # Relief analytics
        try:
            import pandas as pd
            import numpy as np
            df_relief = pd.DataFrame({"step": pl["steps"], "relief": relief_scores})
            st.bar_chart(df_relief.set_index("step"))
            best_idx = int(np.argmax(relief_scores)) if relief_scores else None
            if best_idx is not None:
                st.info(f"Top-performing step: {pl['steps'][best_idx]}")
            # Suggest alternate if low relief
            if any(r <= 4 for r in relief_scores):
                st.warning("Low relief detected. Try swapping in Box Breathing or a short micro-walk next time.")
        except Exception:
            pass

divider_fn()
section_title_fn("Find Support Resources", "🧭")
city = st.text_input("City/ZIP", value=st.session_state.get('city', ''), key="city")
afford = st.selectbox("Affordability", ["Any", "Low-cost", "Insurance"], index=0, key="afford")
language = st.selectbox("Language", ["Any", "English", "Hindi", "Urdu"], index=0, key="language")
remote = st.selectbox("Remote/Online", ["Any", "Yes", "No"], index=0, key="remote")
if st.button("Search Resources"):
    # Mock directory; in production, integrate an API/dataset
    resources = [
        {"name": "Calm Minds Clinic", "type": "Therapist", "city": "Delhi", "afford": "Low-cost", "lang": "Hindi", "remote": "Yes"},
        {"name": "Hope Support Group", "type": "Group", "city": "Mumbai", "afford": "Any", "lang": "English", "remote": "Yes"},
        {"name": "Better Days Telehealth", "type": "Telehealth", "city": "Any", "afford": "Insurance", "lang": "English", "remote": "Yes"},
    ]
    def match(r):
        ok = True
        if city and city.lower() not in (r["city"].lower(), "any"):
            ok = False
        if afford != "Any" and r["afford"] != afford:
            ok = False
        if language != "Any" and r["lang"] != language:
            ok = False
        if remote != "Any" and r["remote"] != remote:
            ok = False
        return ok
    hits = [r for r in resources if match(r)]
    if hits:
        for r in hits:
            st.markdown(f"- **{r['name']}** ({r['type']}) — {r['city']} • {r['afford']} • {r['lang']} • Remote: {r['remote']}")
        st.caption("Tip: When reaching out, you can use this first message:")
        st.code("Hello, I'm looking for support for stress/anxiety. Do you offer sessions that fit low-cost/insurance and remote options?", language="text")
    else:
        st.warning("No matches. Try broadening filters or remote options.")

divider_fn()
section_title_fn("Weekly Check-in", "📈")
check_col1, check_col2, check_col3 = st.columns(3)
with check_col1:
    mood = st.slider("Mood (1–10)", 1, 10, 5)
with check_col2:
    sleep = st.slider("Sleep hours", 0, 12, 7)
with check_col3:
    stress = st.slider("Stress (1–10)", 1, 10, 5)
if 'checkins' not in st.session_state:
    st.session_state['checkins'] = []
if st.button("Add Check-in"):
    st.session_state['checkins'].append({"mood": mood, "sleep": sleep, "stress": stress})
    st.success("Check-in added.")
if st.session_state['checkins']:
    import pandas as pd
    df = pd.DataFrame(st.session_state['checkins'])
    st.line_chart(df)
    st.caption("Trend of mood, sleep, and stress over your check-ins.")
    st.info("Reminder: You can revisit weekly and add a new check-in.")

    # --- New: Insights & Smart Nudges ---
    st.subheader("Insights & Smart Nudges")
    try:
        corr = df.corr(numeric_only=True)
        # Extract simple pair correlations
        cm = {
            "mood~sleep": float(corr.loc["mood", "sleep"]) if "mood" in corr.index and "sleep" in corr.columns else None,
            "mood~stress": float(corr.loc["mood", "stress"]) if "mood" in corr.index and "stress" in corr.columns else None,
            "sleep~stress": float(corr.loc["sleep", "stress"]) if "sleep" in corr.index and "stress" in corr.columns else None,
        }
        msgs = []
        if cm["mood~sleep"] is not None and cm["mood~sleep"] > 0.3:
            msgs.append("Better sleep correlates with improved mood.")
        if cm["mood~stress"] is not None and cm["mood~stress"] < -0.3:
            msgs.append("Higher stress correlates with lower mood.")
        if cm["sleep~stress"] is not None and cm["sleep~stress"] < -0.3:
            msgs.append("More sleep correlates with less stress.")
        if msgs:
            st.success("Insights: " + " ".join(msgs))
        else:
            st.caption("Not enough data for strong insights yet. Keep logging!")
    except Exception:
        st.caption("Insights unavailable. Add more check-ins to enable analytics.")

    nudges_enabled = st.checkbox("Enable gentle nudges (local-only)", value=st.session_state.get("nudges_enabled", False), key="nudges_enabled")
    if nudges_enabled:
        # Simple, local suggestion based on latest check-in
        last = df.iloc[-1]
        suggestions = []
        if last.get("sleep", 7) <= 5:
            suggestions.append("Try an earlier wind-down with device-off + dim lights.")
        if last.get("stress", 5) >= 7:
            suggestions.append("Do a grounding session and send one supportive text.")
        if last.get("mood", 5) <= 4:
            suggestions.append("Plan a 10-min walk and note one positive moment.")
        if suggestions:
            st.warning("Today’s nudge: " + " ".join(suggestions))
        else:
            st.info("No strong nudge needed today. Keep steady!")

divider_fn()
section_title_fn("Crisis Readiness Card", "🆘")
warn = st.text_area("Warning signs you notice")
supports = st.text_area("People to contact (names + numbers)")
steps = st.text_area("If I notice warning signs, I will…")
if st.button("Create Safety Card"):
    card = f"""
Safety Card\n\nWarning signs:\n{warn}\n\nSupports to contact:\n{supports}\n\nPlan:\n{steps}\n\nEmergency: 988 (US), 112/999 (local), or nearest emergency services.
"""
    st.session_state['safety_card'] = card
    st.success("Safety card ready. You can copy/save it.")
if st.session_state.get('safety_card'):
    st.text_area("Your Safety Card", st.session_state['safety_card'], height=200)
    st.download_button(
        label="Download Safety Card",
        data=st.session_state['safety_card'],
        file_name="safety_card.txt",
        mime="text/plain",
    )

divider_fn()
section_title_fn("Personalized Care Pathways", "🛤️")
if st.session_state.get("highlight_care_path"):
    st.info("Start by choosing a duration and focus — your care path will adapt.")
    st.session_state["highlight_care_path"] = False
path_len = st.selectbox("Path duration", ["2 weeks", "3 weeks", "4 weeks"], index=1, key="path_len")
focus = st.selectbox("Primary focus", [
    "Sleep regulation",
    "Anxiety management",
    "Burnout recovery",
    "Depression support",
    "General wellbeing",
], key="focus")

def build_path(duration_weeks: int, focus_area: str, phq_total: int = 0, gad_total: int = 0):
    days = duration_weeks * 7
    steps = []
    for d in range(1, days + 1):
        if focus_area == "Sleep regulation":
            steps.append(f"Day {d}: Fixed bedtime + device-off 30m before sleep; 5-min breathwork.")
        elif focus_area == "Anxiety management":
            steps.append(f"Day {d}: 5-4-3-2-1 grounding + 4x box breathing; log one worry and reframe.")
        elif focus_area == "Burnout recovery":
            steps.append(f"Day {d}: 10-min walk + one boundary action (say no/delegate); gratitude 3 lines.")
        elif focus_area == "Depression support":
            steps.append(f"Day {d}: 1 small activity (shower/dish), 5-min sunlight, text one supportive person.")
        else:
            steps.append(f"Day {d}: 3-min habit: stretch + breath + one positive note.")
    # Tailor intensity based on scores
    note = ""
    if phq_total >= 15 or gad_total >= 15:
        note = "High symptom levels detected — prioritize minimal, doable steps and consider professional support."
    elif phq_total >= 10 or gad_total >= 10:
        note = "Moderate levels — add one optional support contact per week."
    else:
        note = "Keep consistency; celebrate small wins each week."
    return steps, note

duration_weeks = int(path_len.split(" ")[0])
# Try to reuse PHQ/GAD totals if they exist in the widget keys
phq_total_val = 0
gad_total_val = 0
try:
    phq_total_val = sum(int(st.session_state.get(f"phq_{i}", "0 - Not at all").split(" ")[0]) for i in range(9))
    gad_total_val = sum(int(st.session_state.get(f"gad_{i}", "0 - Not at all").split(" ")[0]) for i in range(7))
except Exception:
    pass

path_steps, path_note = build_path(duration_weeks, focus, phq_total_val, gad_total_val)
if st.button("Generate Care Path"):
    st.session_state['care_path'] = {"focus": focus, "note": path_note, "steps": path_steps}
    st.success("Care path generated.")
if st.session_state.get('care_path'):
    st.markdown(f"**Focus:** {st.session_state['care_path']['focus']}")
    st.info(st.session_state['care_path']['note'])
    show_n = st.slider("Show first N days", 7, min(28, len(st.session_state['care_path']['steps'])), 14)
    for s in st.session_state['care_path']['steps'][:show_n]:
        st.markdown(f"- {s}")
    cp_md = (
        "## Care Path\n\n" +
        f"Focus: {st.session_state['care_path']['focus']}\n\n" +
        st.session_state['care_path']['note'] + "\n\n" +
        "\n".join([f"- {x}" for x in st.session_state['care_path']['steps']])
    )
    st.download_button("Download Care Path", cp_md, file_name="care_path.md", mime="text/markdown")

divider_fn()
section_title_fn("Habit Coach", "📆")
if 'habits' not in st.session_state:
    st.session_state['habits'] = []
if 'habit_streak' not in st.session_state:
    st.session_state['habit_streak'] = 0

habit = st.selectbox("Pick a micro-habit", [
    "1 deep-breath cycle",
    "30-second stretch",
    "2-sentence journal",
    "Drink a glass of water",
])
trigger_rule = st.selectbox("Optional trigger rule", [
    "None",
    "If stress ≥7 → suggest grounding",
    "If sleep ≤5 → suggest early wind-down",
    "If mood ≤4 → suggest social contact",
])
if st.button("Log Habit Done"):
    st.session_state['habits'].append({"habit": habit})
    st.session_state['habit_streak'] += 1
    st.success("Nice! Habit logged — streak +1")

st.write(f"Current streak: {st.session_state['habit_streak']} days")
if st.session_state['habits']:
    mosaic = "".join(["🟩" if i % 2 == 0 else "🟦" for i in range(min(30, len(st.session_state['habits'])))])
    st.markdown(f"Streak mosaic: {mosaic}")

# Simple trigger suggestions based on latest check-in
last_check = st.session_state['checkins'][-1] if st.session_state.get('checkins') else None
if trigger_rule != "None" and last_check:
    suggestion = None
    if trigger_rule.startswith("If stress") and last_check['stress'] >= 7:
        suggestion = "Try 5-4-3-2-1 grounding and one supportive text."
    elif trigger_rule.startswith("If sleep") and last_check['sleep'] <= 5:
        suggestion = "Start wind-down 45m earlier; device-off; dim lights."
    elif trigger_rule.startswith("If mood") and last_check['mood'] <= 4:
        suggestion = "Reach out to a friend; 10-min walk; note one positive." 
    if suggestion:
        st.warning(f"Trigger active: {suggestion}")

if st.button("Get Support Plan"):
    if not api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        with st.spinner('🤖 AI Agents are analyzing your situation...'):
            try:
                task = f"""
                Create a comprehensive mental health support plan based on:
                
                Emotional State: {mental_state}
                Sleep: {sleep_pattern} hours per night
                Stress Level: {stress_level}/10
                Support System: {', '.join(support_system) if support_system else 'None reported'}
                Recent Changes: {recent_changes}
                Current Symptoms: {', '.join(current_symptoms) if current_symptoms else 'None reported'}
                """

                system_messages = {
                    "assessment_agent": """
                    You are an experienced mental health professional speaking directly to the user. Your task is to:
                    1. Create a safe space by acknowledging their courage in seeking support
                    2. Analyze their emotional state with clinical precision and genuine empathy
                    3. Ask targeted follow-up questions to understand their full situation
                    4. Identify patterns in their thoughts, behaviors, and relationships
                    5. Assess risk levels with validated screening approaches
                    6. Help them understand their current mental health in accessible language
                    7. Validate their experiences without minimizing or catastrophizing

                    Always use "you" and "your" when addressing the user. Blend clinical expertise with genuine warmth and never rush to conclusions.
                    """,
                    
                    "action_agent": """
                    You are a crisis intervention and resource specialist speaking directly to the user. Your task is to:
                    1. Provide immediate evidence-based coping strategies tailored to their specific situation
                    2. Prioritize interventions based on urgency and effectiveness
                    3. Connect them with appropriate mental health services while acknowledging barriers (cost, access, stigma)
                    4. Create a concrete daily wellness plan with specific times and activities
                    5. Suggest specific support communities with details on how to join
                    6. Balance crisis resources with empowerment techniques
                    7. Teach simple self-regulation techniques they can use immediately

                    Focus on practical, achievable steps that respect their current capacity and energy levels. Provide options ranging from minimal effort to more involved actions.
                    """,
                    
                    "followup_agent": """
                    You are a mental health recovery planner speaking directly to the user. Your task is to:
                    1. Design a personalized long-term support strategy with milestone markers
                    2. Create a progress monitoring system that matches their preferences and habits
                    3. Develop specific relapse prevention strategies based on their unique triggers
                    4. Establish a support network mapping exercise to identify existing resources
                    5. Build a graduated self-care routine that evolves with their recovery
                    6. Plan for setbacks with self-compassion techniques
                    7. Set up a maintenance schedule with clear check-in mechanisms

                    Focus on building sustainable habits that integrate with their lifestyle and values. Emphasize progress over perfection and teach skills for self-directed care.
                    """
                }

                llm_config = {
                    "config_list": [{"model": model_choice, "api_key": api_key}]
                }

                context_variables = {
                    "assessment": None,
                    "action": None,
                    "followup": None,
                }

                def update_assessment_overview(assessment_summary: str, context_variables: dict) -> SwarmResult:
                    context_variables["assessment"] = assessment_summary
                    st.sidebar.success('Assessment: ' + assessment_summary)
                    return SwarmResult(agent="action_agent", context_variables=context_variables)

                def update_action_overview(action_summary: str, context_variables: dict) -> SwarmResult:
                    context_variables["action"] = action_summary
                    st.sidebar.success('Action Plan: ' + action_summary)
                    return SwarmResult(agent="followup_agent", context_variables=context_variables)

                def update_followup_overview(followup_summary: str, context_variables: dict) -> SwarmResult:
                    context_variables["followup"] = followup_summary
                    st.sidebar.success('Follow-up Strategy: ' + followup_summary)
                    return SwarmResult(agent="assessment_agent", context_variables=context_variables)

                def update_system_message_func(agent: SwarmAgent, messages) -> str:
                    system_prompt = system_messages[agent.name]
                    current_gen = agent.name.split("_")[0]
                    
                    if agent._context_variables.get(current_gen) is None:
                        system_prompt += f"Call the update function provided to first provide a 2-3 sentence summary of your ideas on {current_gen.upper()} based on the context provided."
                        agent.llm_config['tool_choice'] = {"type": "function", "function": {"name": f"update_{current_gen}_overview"}}
                    else:
                        agent.llm_config["tools"] = None
                        agent.llm_config['tool_choice'] = None
                        system_prompt += f"\n\nYour task\nYou task is write the {current_gen} part of the report. Do not include any other parts. Do not use XML tags.\nStart your reponse with: '## {current_gen.capitalize()} Design'."    
                        k = list(agent._oai_messages.keys())[-1]
                        agent._oai_messages[k] = agent._oai_messages[k][:1]

                    system_prompt += f"\n\n\nBelow are some context for you to refer to:"
                    for k, v in agent._context_variables.items():
                        if v is not None:
                            system_prompt += f"\n{k.capitalize()} Summary:\n{v}"

                    agent.client = OpenAIWrapper(**agent.llm_config)
                    return system_prompt
                
                if SwarmAgent is not None:
                    state_update = UPDATE_SYSTEM_MESSAGE(update_system_message_func)
                    assessment_agent = SwarmAgent(
                        "assessment_agent", 
                        llm_config=llm_config,
                        functions=update_assessment_overview,
                        update_agent_state_before_reply=[state_update]
                    )

                    action_agent = SwarmAgent(
                        "action_agent",
                        llm_config=llm_config,
                        functions=update_action_overview,
                        update_agent_state_before_reply=[state_update]
                    )

                    followup_agent = SwarmAgent(
                        "followup_agent",
                        llm_config=llm_config,
                        functions=update_followup_overview,
                        update_agent_state_before_reply=[state_update]
                    )

                    assessment_agent.register_hand_off(AFTER_WORK(action_agent))
                    action_agent.register_hand_off(AFTER_WORK(followup_agent))
                    followup_agent.register_hand_off(AFTER_WORK(assessment_agent))

                    result, _, _ = initiate_swarm_chat(
                        initial_agent=assessment_agent,
                        agents=[assessment_agent, action_agent, followup_agent],
                        user_agent=None,
                        messages=task,
                        max_rounds=13,
                    )

                    if hasattr(result, "chat_history") and len(result.chat_history) >= 3:
                        st.session_state.output = {
                            'assessment': result.chat_history[-3]['content'],
                            'action': result.chat_history[-2]['content'],
                            'followup': result.chat_history[-1]['content']
                        }
                    else:
                        st.error("Unexpected swarm response format.")
                        st.session_state.output = {
                            'assessment': '',
                            'action': '',
                            'followup': ''
                        }
                else:
                    if OpenAI is None:
                        raise ImportError("OpenAI client is not installed. Please install 'openai'.")
                    client = OpenAI(api_key=api_key)
                    prompt = f"""
You are a supportive mental health assistant. Based on the user's details, produce three sections:
1) ## Assessment Design
2) ## Action Design
3) ## Followup Design
Keep responses empathetic, practical, and safe.

Details:
{task}
"""
                    completion = client.chat.completions.create(
                        model=model_choice,
                        messages=[
                            {"role": "system", "content": "You are a helpful, empathetic mental health assistant."},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=0.7,
                    )
                    content = completion.choices[0].message.content
                    # Split naive by section headers for display
                    def extract(section_title: str, text: str) -> str:
                        import re
                        pattern = rf"##\s*{section_title}.*?(?=(\n##|\Z))"
                        m = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
                        return m.group(0) if m else ""

                    st.session_state.output = {
                        'assessment': extract('Assessment', content),
                        'action': extract('Action', content),
                        'followup': extract('Followup', content),
                    }

                with st.expander("Situation Assessment"):
                    st.markdown(st.session_state.output['assessment'])

                with st.expander("Action Plan & Resources"):
                    st.markdown(st.session_state.output['action'])

                with st.expander("Long-term Support Strategy"):
                    st.markdown(st.session_state.output['followup'])

                st.success('✨ Mental health support plan generated successfully!')
                success_confetti()
                combined = (
                    ("# Situation Assessment\n\n" + st.session_state.output['assessment']) +
                    ("\n\n# Action Plan & Resources\n\n" + st.session_state.output['action']) +
                    ("\n\n# Long-term Support Strategy\n\n" + st.session_state.output['followup'])
                )
                st.download_button(
                    label="Download Plan (Markdown)",
                    data=combined,
                    file_name="mental_support_plan.md",
                    mime="text/markdown",
                )

                # --- New: Therapist Handoff + Prep Pack ---
                divider_fn()
                section_title_fn("Therapist Handoff + Prep Pack", "🤝")
                # Recompute PHQ/GAD from session if available
                def _sum_scale(prefix: str, n: int) -> int:
                    total = 0
                    for i in range(n):
                        raw = st.session_state.get(f"{prefix}_{i}") or "0 - Not at all"
                        try:
                            total += int(str(raw).split(" ")[0])
                        except Exception:
                            total += 0
                    return total
                phq_total_pp = _sum_scale("phq", 9)
                gad_total_pp = _sum_scale("gad", 7)
                def _sev(score: int, kind: str) -> str:
                    if kind == "phq":
                        return (
                            "Minimal (0–4)" if score <= 4 else
                            "Mild (5–9)" if score <= 9 else
                            "Moderate (10–14)" if score <= 14 else
                            "Moderately severe (15–19)" if score <= 19 else
                            "Severe (20–27)"
                        )
                    else:
                        return (
                            "Minimal (0–4)" if score <= 4 else
                            "Mild (5–9)" if score <= 9 else
                            "Moderate (10–14)" if score <= 14 else
                            "Severe (15–21)"
                        )

                overview = (st.session_state.get("mental_state") or "").strip()
                changes = (st.session_state.get("recent_changes") or "").strip()
                symptoms_list = st.session_state.get("current_symptoms") or []
                safety_present = bool(st.session_state.get("safety_card"))
                care_focus = st.session_state.get("care_path", {}).get("focus", "")

                # Build a de-identified prep summary
                prep_md = """## Therapy Prep Summary (De-identified)

### Overview
- Emotional state: {}{}
- Recent changes: {}
- Current symptoms: {}

### Screening
- PHQ-9 total: {} ({})
- GAD-7 total: {} ({})

### Safety
- Safety card present: {}

### Goals (first sessions)
- Clarify top concerns and triggers
- Agree on 2–3 priorities for next 2–4 weeks{}
- Identify quick wins and support constraints (time, cost, access)

### Current Plan Snapshot
- Assessment: (see attachment or section in app)
- Action plan: (see attachment or section in app)
- Follow-up: (see attachment or section in app)

> Note: This summary avoids personal identifiers and is intended to speed up your first therapy session. You can edit it before sharing.
""".format(
                    overview[:300] + ("…" if len(overview) > 300 else ""),
                    "" if overview else "(not provided)",
                    changes[:300] + ("…" if len(changes) > 300 else ""),
                    ", ".join(symptoms_list) if symptoms_list else "(none provided)",
                    phq_total_pp, _sev(phq_total_pp, "phq"),
                    gad_total_pp, _sev(gad_total_pp, "gad"),
                    "Yes" if safety_present else "No",
                    f" (focus: {care_focus})" if care_focus else "",
                )

                st.markdown(prep_md)
                st.download_button(
                    label="Download Therapy Prep (Markdown)",
                    data=prep_md,
                    file_name="therapy_prep_summary.md",
                    mime="text/markdown",
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
