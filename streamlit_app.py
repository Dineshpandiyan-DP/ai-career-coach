import streamlit as st
import requests
import json

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerAI — Your AI Career Coach",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}  # hide hamburger menu
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --navy:    #0f2240;
    --emerald: #059669;
    --amber:   #f59e0b;
    --rose:    #e11d48;
    --bg:      #f8f7f4;
    --surface: #ffffff;
    --border:  #e5e2db;
    --muted:   #7a7566;
    --text:    #1a1814;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text);
}

/* ── Base ── */
.stApp {
    background: var(--bg);
    background-image: radial-gradient(circle at 80% 0%, #e8f5f0 0%, transparent 50%),
                      radial-gradient(circle at 0% 100%, #fdf3e3 0%, transparent 40%);
}

#MainMenu, footer, header { visibility: hidden; }

/* ── Kill Streamlit's built-in top padding ── */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}



/* Sidebar top padding fix — collapse button is hidden so we can go tighter */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem !important;
}

/* Hide sidebar collapse button only */
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--navy) !important;
    min-width: 320px !important;
    max-width: 320px !important;
    width: 320px !important;
    border-right: none !important;

    display: block !important;
    visibility: visible !important;
    transform: none !important;
    z-index: 999 !important;
}

section[data-testid="stSidebar"] > div {
    background: var(--navy) !important;
    min-width: 320px !important;
    max-width: 320px !important;
    width: 320px !important;
    height: 100vh !important;
    padding-top: 0.5rem !important;
}

[data-testid="stSidebar"] * {
    color: #d4dce8 !important;
}

/* ── Hero ── */
.hero-wrap {
    padding: 0.8rem 0 1.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}

.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--emerald);
    margin-bottom: 0.5rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: var(--navy);
    line-height: 1.08;
    margin-bottom: 0.6rem;
}

.hero-title span {
    color: var(--emerald);
}

.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 400;
    max-width: 520px;
    line-height: 1.7;
}

/* ── Section header ── */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--navy);
    margin-bottom: 0.3rem;
}

.section-desc {
    font-size: 0.9rem;
    color: var(--muted);
    margin-bottom: 1.8rem;
    line-height: 1.6;
}

/* ── Pill label ── */
.pill {
    display: inline-block;
    background: #ecfdf5;
    color: var(--emerald);
    border: 1px solid #a7f3d0;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 12px;
    margin-bottom: 1rem;
}

/* ── Metric cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.5rem;
    flex: 1;
    text-align: center;
    box-shadow: 0 2px 8px rgba(15,34,64,0.05);
    transition: box-shadow 0.2s;
}

.metric-card:hover {
    box-shadow: 0 6px 20px rgba(15,34,64,0.10);
}

.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--navy);
}

.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* ── Result box ── */
.result-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--emerald);
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    margin-top: 1rem;
    box-shadow: 0 2px 12px rgba(15,34,64,0.06);
}

/* ── Tip box ── */
.tip-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.88rem;
    color: #78350f;
    margin-top: 1rem;
}

/* ── Status indicators ── */
.status-online {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-radius: 10px;
    padding: 0.75rem 1rem;
}

.status-offline {
    background: #fff1f2;
    border: 1px solid #fda4af;
    border-radius: 10px;
    padding: 0.75rem 1rem;
}

/* ── Input overrides ── */
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.93rem !important;
    transition: border-color 0.2s !important;
}

.stTextArea textarea:focus {
    border-color: var(--emerald) !important;
    box-shadow: 0 0 0 3px rgba(5,150,105,0.1) !important;
}

.stTextInput input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: border-color 0.2s !important;
}

.stTextInput input:focus {
    border-color: var(--emerald) !important;
    box-shadow: 0 0 0 3px rgba(5,150,105,0.1) !important;
}

.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

.stNumberInput input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

.stMultiSelect > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
}

.stSlider > div > div > div {
    background: var(--emerald) !important;
}

/* Labels */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label,
.stMultiSelect label, .stSlider label {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: var(--navy) !important;
    margin-bottom: 0.3rem !important;
}

/* ── Button ── */
.stButton > button {
    background: var(--navy) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 4px 14px rgba(15,34,64,0.25) !important;
}

.stButton > button:hover {
    background: #1a3a6e !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(15,34,64,0.35) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid var(--border);
    gap: 0;
    margin-bottom: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.7rem 1.5rem;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: color 0.2s;
}

.stTabs [aria-selected="true"] {
    color: var(--navy) !important;
    border-bottom: 2px solid var(--navy) !important;
    background: transparent !important;
}

/* ── Alert overrides ── */
.stSuccess {
    background: #ecfdf5 !important;
    border: 1px solid #a7f3d0 !important;
    color: #065f46 !important;
    border-radius: 10px !important;
}

.stError {
    background: #fff1f2 !important;
    border: 1px solid #fda4af !important;
    color: #9f1239 !important;
    border-radius: 10px !important;
}

.stInfo {
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    color: #1e40af !important;
    border-radius: 10px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--emerald) !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
BASE_URL = st.secrets.get("BASE_URL", "http://127.0.0.1:8000")
API_URL = f"{BASE_URL}/agent"

SKILLS_OPTIONS = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "Statistics",
    "EDA", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
    "Docker", "AWS", "GCP", "FastAPI", "Flask", "Spark", "Hadoop",
    "Tableau", "Power BI", "NLP", "Computer Vision", "MLflow",
    "LangChain", "Git", "Linux", "R", "Java", "JavaScript", "React"
]

# ── Helper ─────────────────────────────────────────────────────────────────────
def call_api(tool: str, payload: dict):
    try:
        res = requests.post(API_URL, json={"tool": tool, "payload": payload}, timeout=60)
        res.raise_for_status()
        return res.json(), None
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to backend. Make sure FastAPI is running on port 8000."
    except requests.exceptions.Timeout:
        return None, "❌ Request timed out. The AI is taking too long, please try again."
    except Exception as e:
        return None, f"❌ Error: {str(e)}"


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 0 1rem 0;'>
        <div style='font-size:0.68rem; font-weight:700; letter-spacing:0.18em;
                    text-transform:uppercase; color:#6ee7b7; margin-bottom:0.5rem;'>
            AI-POWERED
        </div>
        <div style='font-family: "Playfair Display", serif; font-size: 1.55rem;
                    font-weight: 900; color: #ffffff; line-height:1.15;'>
            Career<br><span style='color:#6ee7b7;'>Coach</span>
        </div>
        <div style='font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem;'>
            Powered by Groq · Llama 3.3-70b
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:0.5rem 0 1rem 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size:0.68rem; font-weight:700; letter-spacing:0.14em;
                text-transform:uppercase; color:#64748b; margin-bottom:0.9rem;'>
        Available Tools
    </div>
    """, unsafe_allow_html=True)

    tools_info = [
        ("📄", "Resume Review", "ATS score + deep feedback", "#6ee7b7", "#065f46"),
        ("🎤", "Mock Interview", "Practice Q&A with scoring", "#93c5fd", "#1e3a5f"),
        ("🗺️", "Learning Roadmap", "Week-by-week skill plan", "#fcd34d", "#78350f"),
    ]
    for icon, name, desc, accent, text_col in tools_info:
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.09);
                    border-left: 3px solid {accent};
                    border-radius: 10px; padding: 0.85rem 1rem; margin-bottom: 0.6rem;'>
            <div style='font-weight: 600; font-size: 0.88rem; color: #f1f5f9;'>
                {icon} &nbsp;{name}
            </div>
            <div style='font-size: 0.75rem; color: #94a3b8; margin-top: 0.2rem;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:1rem 0;'>", unsafe_allow_html=True)

    # Backend status
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=3)
        if health.status_code == 200:
            data = health.json()
            st.markdown(f"""
            <div class='status-online' style='background:rgba(110,231,183,0.12); border:1px solid rgba(110,231,183,0.25); border-radius:10px; padding:0.75rem 1rem;'>
                <div style='color:#6ee7b7; font-size:0.8rem; font-weight:700;'>● Backend Online</div>
                <div style='color:#94a3b8; font-size:0.72rem; margin-top:0.2rem;'>
                    Model: {data.get('model', 'unknown')}
                </div>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div style='background:rgba(253,164,175,0.12); border:1px solid rgba(253,164,175,0.25);
                    border-radius:10px; padding:0.75rem 1rem;'>
            <div style='color:#fda4af; font-size:0.8rem; font-weight:700;'>● Backend Offline</div>
            <div style='color:#94a3b8; font-size:0.72rem; margin-top:0.3rem;'>
                Run: <code style='background:rgba(255,255,255,0.1); padding:1px 5px; border-radius:4px;'>uvicorn app.main:app --reload</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:auto; padding-top:2rem; font-size:0.72rem; color:#475569; text-align:center;'>
        © 2025 CareerAI &nbsp;·&nbsp; v1.0
    </div>
    """, unsafe_allow_html=True)


# ── Main Content ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap'>
    <div class='hero-eyebrow'>✦ AI-Powered Career Acceleration</div>
    <div class='hero-title'>Land Your <span>Dream Role</span><br>With AI Coaching</div>
    <div class='hero-sub'>Get instant ATS analysis, practice real interview questions, and receive a personalized learning roadmap — all in one place.</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📄  Resume Review", "🎤  Mock Interview", "🗺️  Learning Roadmap"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RESUME REVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class='pill'>Resume Analysis</div>
    <div class='section-header'>Resume Review</div>
    <div class='section-desc'>Paste your resume and target role to get an ATS compatibility score, key strengths, critical gaps, and missing keywords — all in seconds.</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        target_role = st.text_input("🎯 Target Role", placeholder="e.g. Data Scientist, ML Engineer")
        years_exp = st.number_input("📅 Years of Experience", min_value=0, max_value=30, value=3)
        resume_text = st.text_area(
            "📋 Paste Your Resume",
            height=300,
            placeholder="Paste your full resume text here..."
        )

    with col2:
        job_description = st.text_area(
            "💼 Job Description (optional)",
            height=390,
            placeholder="Paste the job description you're applying for to get role-specific feedback..."
        )

    if st.button("🔍 Analyze My Resume", key="resume_btn"):
        if not resume_text.strip():
            st.error("Please paste your resume text.")
        elif not target_role.strip():
            st.error("Please enter your target role.")
        else:
            with st.spinner("Analyzing your resume with AI…"):
                payload = {
                    "resume_text": resume_text,
                    "target_role": target_role,
                    "years_of_experience": years_exp,
                }
                if job_description.strip():
                    payload["job_description"] = job_description

                data, error = call_api("resume_review", payload)

            if error:
                st.error(error)
            else:
                st.success("✅ Analysis complete!")

                st.markdown(f"""
                <div class='metric-row'>
                    <div class='metric-card'>
                        <div class='metric-value'>{data.get('tokens_used', 0)}</div>
                        <div class='metric-label'>Tokens Used</div>
                    </div>
                    <div class='metric-card'>
                        <div class='metric-value' style='color:#059669'>{data.get('model', '').split('-')[0].upper()}</div>
                        <div class='metric-label'>Model</div>
                    </div>
                    <div class='metric-card'>
                        <div class='metric-value' style='color:#0f2240; font-size:1.2rem'>{target_role.split()[0]}</div>
                        <div class='metric-label'>Target Role</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='section-header' style='font-size:1.2rem; margin-top:0.5rem;'>📊 Analysis Result</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-box'>{data.get('result', '')}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MOCK INTERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class='pill'>Interview Practice</div>
    <div class='section-header'>Mock Interview</div>
    <div class='section-desc'>Simulate a real interview with role-specific questions, AI feedback, and scoring. Iterate until you feel confident.</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        interview_role = st.text_input("🎯 Job Role", placeholder="e.g. Data Scientist", key="int_role")
        experience_level = st.selectbox(
            "📊 Experience Level",
            options=["junior", "mid", "senior"],
            index=1
        )
        topic = st.text_input(
            "📚 Topic Focus (optional)",
            placeholder="e.g. Machine Learning, SQL, System Design"
        )

    with col2:
        previous_answer = st.text_area(
            "💬 Your Answer to Previous Question",
            height=220,
            placeholder="Leave empty to start a fresh session.\n\nAfter your first question arrives, write your answer here and click the button again to get feedback and the next question."
        )

    if st.button("🎤 Start / Continue Interview", key="interview_btn"):
        if not interview_role.strip():
            st.error("Please enter the job role.")
        else:
            with st.spinner("AI interviewer is preparing your question…"):
                payload = {
                    "role": interview_role,
                    "experience_level": experience_level,
                }
                if topic.strip():
                    payload["topic"] = topic
                if previous_answer.strip():
                    payload["previous_answer"] = previous_answer

                data, error = call_api("mock_interview", payload)

            if error:
                st.error(error)
            else:
                st.success("✅ Interviewer responded!")

                st.markdown(f"""
                <div class='metric-row'>
                    <div class='metric-card'>
                        <div class='metric-value'>{data.get('tokens_used', 0)}</div>
                        <div class='metric-label'>Tokens Used</div>
                    </div>
                    <div class='metric-card'>
                        <div class='metric-value' style='color:#059669'>{experience_level.upper()}</div>
                        <div class='metric-label'>Level</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='section-header' style='font-size:1.2rem; margin-top:0.5rem;'>🎙️ Interviewer</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-box'>{data.get('result', '')}</div>", unsafe_allow_html=True)

                st.markdown("""
                <div class='tip-box'>
                    💡 <strong>Next step:</strong> Copy the question above, write your answer, paste it in the "Your Answer" field, and click the button again to continue the session.
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — LEARNING ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class='pill'>Skill Planning</div>
    <div class='section-header'>Learning Roadmap</div>
    <div class='section-desc'>Tell us where you are and where you want to go. Get a structured, week-by-week learning plan tailored to your existing skills and timeline.</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        roadmap_role = st.text_input("🎯 Target Role", placeholder="e.g. AI Engineer, Data Scientist", key="rm_role")
        available_weeks = st.slider("📅 Available Weeks", min_value=4, max_value=24, value=12, step=2)
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:0.6rem; margin-top:-0.4rem; margin-bottom:1rem;'>
            <span style='font-size:0.85rem; color:#059669; font-weight:600;'>
                ⏱ {available_weeks} weeks &nbsp;·&nbsp; ~{available_weeks // 4} month{'s' if available_weeks // 4 != 1 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        current_skills = st.multiselect(
            "🛠️ Your Current Skills",
            options=SKILLS_OPTIONS,
            default=["Python", "SQL", "Machine Learning"],
            help="Select all skills you already have"
        )
        extra_skills = st.text_input(
            "➕ Other Skills (comma-separated)",
            placeholder="e.g. Spark, Airflow, dbt"
        )

    if st.button("🗺️ Generate My Roadmap", key="roadmap_btn"):
        if not roadmap_role.strip():
            st.error("Please enter your target role.")
        elif not current_skills and not extra_skills.strip():
            st.error("Please select at least one current skill.")
        else:
            all_skills = list(current_skills)
            if extra_skills.strip():
                extras = [s.strip() for s in extra_skills.split(",") if s.strip()]
                all_skills.extend(extras)

            with st.spinner(f"Building your {available_weeks}-week personalized roadmap…"):
                payload = {
                    "target_role": roadmap_role,
                    "current_skills": all_skills,
                    "available_weeks": available_weeks,
                }
                data, error = call_api("learning_roadmap", payload)

            if error:
                st.error(error)
            else:
                st.success("✅ Roadmap generated!")

                st.markdown(f"""
                <div class='metric-row'>
                    <div class='metric-card'>
                        <div class='metric-value'>{data.get('tokens_used', 0)}</div>
                        <div class='metric-label'>Tokens Used</div>
                    </div>
                    <div class='metric-card'>
                        <div class='metric-value' style='color:#059669'>{available_weeks}w</div>
                        <div class='metric-label'>Duration</div>
                    </div>
                    <div class='metric-card'>
                        <div class='metric-value' style='color:#0f2240'>{len(all_skills)}</div>
                        <div class='metric-label'>Skills Found</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div class='section-header' style='font-size:1.2rem; margin-top:0.5rem;'>🗺️ Your Personalized Roadmap</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-box'>{data.get('result', '')}</div>", unsafe_allow_html=True)