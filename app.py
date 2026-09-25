"""
Resume-to-Interview Questions Generator - Streamlit frontend

Run:
    pip install streamlit requests pandas
    streamlit run app.py

Backend is expected at http://localhost:8000 (editable in the sidebar).
"""

import requests
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Config - change these if your backend differs
# ---------------------------------------------------------------------------
DEFAULT_API_URL = "http://localhost:8000"
UPLOAD_FIELD_NAME = "file"   # multipart field name for the PDF in POST /upload-resume
REQUEST_TIMEOUT = 120        # seconds; scoring by an LLM can be slow

st.set_page_config(
    page_title="Resume Interview Generator",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Visual theme (CSS only - no logic here)
# ---------------------------------------------------------------------------
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
        h1, h2, h3, .hero-title { font-family: 'Sora', sans-serif; }

        /* ---- Hero header ---- */
        .hero {
            padding: 2.2rem 2.4rem;
            border-radius: 14px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border: 1px solid rgba(148,163,184,0.25);
            color: #f1f5f9;
            margin-bottom: 1.6rem;
        }
        .hero-title {
            font-size: 1.7rem; font-weight: 700; margin: 0 0 .4rem 0;
            letter-spacing: -0.3px;
        }
        .hero-sub { font-size: 0.95rem; color: #94a3b8; margin: 0; }
        .hero-tags { margin-top: 1rem; }
        .hero-tag {
            display: inline-block; background: rgba(99,102,241,0.15);
            color: #a5b4fc; padding: 4px 12px; border-radius: 6px;
            font-size: 0.75rem; font-weight: 600; letter-spacing: 0.3px;
            text-transform: uppercase; margin-right: 8px;
            border: 1px solid rgba(99,102,241,0.3);
        }

        /* ---- Generic card ---- */
        .card {
            border: 1px solid rgba(148,163,184,0.25);
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.9rem;
        }

        /* ---- Question card ---- */
        .q-card {
            border-radius: 12px;
            padding: 1.4rem 1.5rem;
            border: 1px solid rgba(99,102,241,0.35);
            border-left: 4px solid #6366f1;
            margin-bottom: 1rem;
        }
        .q-text { font-size: 1.05rem; font-weight: 500; line-height: 1.55; margin-bottom: 1rem; }
        .meta-row { display: flex; gap: 0.5rem; flex-wrap: wrap; }
        .pill {
            display: inline-block; padding: 4px 11px; border-radius: 6px;
            font-size: 0.74rem; font-weight: 600; letter-spacing: 0.2px;
            border: 1px solid transparent;
        }
        .pill-topic   { background: rgba(99,102,241,0.12); color: #818cf8; border-color: rgba(99,102,241,0.3); }
        .pill-domain  { background: rgba(14,165,233,0.12); color: #38bdf8; border-color: rgba(14,165,233,0.3); }
        .pill-easy    { background: rgba(34,197,94,0.14);  color: #4ade80; border-color: rgba(34,197,94,0.3); }
        .pill-medium  { background: rgba(234,179,8,0.16);  color: #facc15; border-color: rgba(234,179,8,0.3); }
        .pill-hard    { background: rgba(239,68,68,0.14);  color: #f87171; border-color: rgba(239,68,68,0.3); }
        .pill-default { background: rgba(148,163,184,0.14); color: #94a3b8; border-color: rgba(148,163,184,0.3); }

        /* ---- Score card ---- */
        .score-card {
            border-radius: 12px;
            padding: 1.3rem 1.5rem;
            border: 1px solid rgba(148,163,184,0.25);
            border-left: 4px solid #22c55e;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1.6rem;
        }
        .score-big { font-size: 2.2rem; font-weight: 700; font-family: 'Sora', sans-serif; }
        .score-label { font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.6px; }
        .score-domain { font-size: 0.88rem; color: #cbd5e1; }

        /* ---- Section title with accent bar ---- */
        .section-title {
            font-family: 'Sora', sans-serif; font-weight: 600; font-size: 1.0rem;
            border-left: 3px solid #6366f1; padding-left: 10px; margin: 0.4rem 0 0.8rem 0;
            text-transform: uppercase; letter-spacing: 0.4px;
        }

        /* ---- Sidebar polish ---- */
        section[data-testid="stSidebar"] { border-right: 1px solid rgba(148,163,184,0.2); }
        .sidebar-tag {
            font-size: 0.72rem; font-weight: 700; letter-spacing: 0.6px;
            text-transform: uppercase; color: #818cf8; margin-bottom: 6px; display: block;
        }
        .session-box {
            border: 1px solid rgba(34,197,94,0.3); border-left: 3px solid #22c55e;
            border-radius: 8px; padding: 0.7rem 0.9rem; margin-top: 0.4rem;
        }

        /* ---- Buttons ---- */
        .stButton > button {
            border-radius: 8px; font-weight: 600; border: 1px solid rgba(99,102,241,0.4);
            background: #6366f1; color: white; transition: 0.15s ease-in-out;
        }
        .stButton > button:hover { background: #4f46e5; border-color: #4f46e5; }

        /* ---- Tabs ---- */
        .stTabs [data-baseweb="tab"] { font-weight: 600; font-family: 'Inter', sans-serif; }

        /* Chip list for skills */
        .chip {
            display:inline-block; background: rgba(99,102,241,0.10); color:#818cf8;
            padding: 5px 12px; border-radius: 6px; font-size: 0.78rem; margin: 3px 4px 3px 0;
            border: 1px solid rgba(99,102,241,0.25);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "user_id": "",
        "session_id": None,
        "question": None,       # current question (normalized)
        "last_result": None,    # result of the last submitted answer
        "skills": [],
        "projects": [],
        "dsa_weight": 0.5,
        "answered": 0,
        "finished": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def normalize_question(q):
    """The contract mixes question/questions and topic/topics - accept both."""
    if not q:
        return None
    return {
        "id": q.get("id"),
        "question": q.get("question") or q.get("questions") or "",
        "topic": q.get("topic") or q.get("topics") or "",
        "domain": q.get("domain") or "",
        "difficulty": q.get("difficulty") or "",
    }


def call_api(method, path, **kwargs):
    """Returns (data, error_message). Exactly one of them is None."""
    url = f"{st.session_state.api_url.rstrip('/')}{path}"
    try:
        response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
    except requests.exceptions.ConnectionError:
        return None, f"Cannot connect to the backend at {st.session_state.api_url}. Is it running?"
    except requests.exceptions.Timeout:
        return None, "The backend took too long to respond."
    except requests.exceptions.RequestException as exc:
        return None, f"Request failed: {exc}"

    if not response.ok:
        return None, f"Backend returned {response.status_code}: {response.text}"
    try:
        return response.json(), None
    except ValueError:
        return None, "Backend did not return valid JSON."


def label(key):
    return key.replace("_", " ").title()


def difficulty_pill_class(difficulty):
    d = (difficulty or "").strip().lower()
    if d == "easy":
        return "pill-easy"
    if d == "medium":
        return "pill-medium"
    if d == "hard":
        return "pill-hard"
    return "pill-default"


def show_question(q):
    diff_class = difficulty_pill_class(q["difficulty"])
    st.markdown(
        f"""
        <div class="q-card">
            <div class="q-text">{q['question']}</div>
            <div class="meta-row">
                <span class="pill pill-topic">TOPIC: {q['topic'] or '-'}</span>
                <span class="pill pill-domain">DOMAIN: {q['domain'] or '-'}</span>
                <span class="pill {diff_class}">DIFFICULTY: {q['difficulty'] or '-'}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_result(result):
    st.markdown('<div class="section-title">Result of your last answer</div>', unsafe_allow_html=True)

    score = result.get("score", "-")
    domain = result.get("domain", "")
    st.markdown(
        f"""
        <div class="score-card">
            <div>
                <div class="score-label">Score</div>
                <div class="score-big">{score}</div>
            </div>
            <div class="score-domain">Domain<br><b>{domain}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    breakdown = result.get("breakdown") or {}
    if breakdown:
        cols = st.columns(len(breakdown))
        for col, (key, value) in zip(cols, breakdown.items()):
            col.metric(label(key), value)

    st.markdown("**Feedback**")
    st.info(result.get("feedback") or "No feedback available.")


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
init_state()
inject_css()

st.sidebar.markdown('<span class="sidebar-tag">Settings</span>', unsafe_allow_html=True)
st.session_state.setdefault("api_url", DEFAULT_API_URL)
st.sidebar.text_input("Backend URL", key="api_url")

st.sidebar.text_input(
    "User ID",
    key="user_id",
    help="Filled automatically after a resume upload. Enter an existing ID to continue as a returning user.",
)

st.sidebar.divider()
st.sidebar.markdown('<span class="sidebar-tag">Domain mix</span>', unsafe_allow_html=True)
st.sidebar.slider("DSA weight", 0.0, 1.0, step=0.05, key="dsa_weight")
ai_ml_weight = round(1.0 - st.session_state.dsa_weight, 2)
st.sidebar.progress(
    st.session_state.dsa_weight,
    text=f"DSA {st.session_state.dsa_weight:.2f}  /  AI-ML {ai_ml_weight:.2f}",
)

if st.session_state.session_id:
    st.sidebar.divider()
    st.sidebar.markdown('<span class="sidebar-tag">Live session</span>', unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <div class="session-box">
            <code style="font-size:0.78rem;">{st.session_state.session_id}</code><br>
            <span style="font-size:0.8rem; color:#94a3b8;">Questions answered: <b>{st.session_state.answered}</b></span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.sidebar.button("End session"):
        st.session_state.session_id = None
        st.session_state.question = None
        st.session_state.last_result = None
        st.session_state.answered = 0
        st.session_state.finished = False
        st.rerun()

st.sidebar.divider()
st.sidebar.caption("Streamlit frontend - LLM scoring backend")


# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Resume-to-Interview Questions Generator</div>
        <p class="hero-sub">Upload a resume, run a tailored DSA / AI-ML interview, and track improvement over time.</p>
        <div class="hero-tags">
            <span class="hero-tag">Resume Parsing</span>
            <span class="hero-tag">Adaptive Questions</span>
            <span class="hero-tag">Progress Tracking</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_upload, tab_start, tab_interview, tab_progress = st.tabs(
    ["Upload Resume", "Start Interview", "Interview", "Progress"]
)

# ---- Upload ---------------------------------------------------------------
with tab_upload:
    st.markdown('<div class="section-title">Upload your resume</div>', unsafe_allow_html=True)
    pdf = st.file_uploader("PDF resume", type=["pdf"])

    if st.button("Upload resume", disabled=pdf is None):
        files = {UPLOAD_FIELD_NAME: (pdf.name, pdf.getvalue(), "application/pdf")}
        with st.spinner("Analysing resume..."):
            data, error = call_api("POST", "/upload-resume", files=files)
        if error:
            st.error(error)
        else:
            st.session_state.user_id = data.get("user_id", st.session_state.user_id)
            st.session_state.skills = data.get("skills", [])
            st.session_state.projects = data.get("projects", [])
            weights = data.get("domain_weights") or {}
            if "dsa" in weights:
                st.session_state.dsa_weight = float(weights["dsa"])
            st.rerun()

    if st.session_state.skills or st.session_state.projects:
        st.success(f"Resume processed. Your user ID: `{st.session_state.user_id}`")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="section-title">Detected skills</div>', unsafe_allow_html=True)
            if st.session_state.skills:
                chips = "".join(f'<span class="chip">{s}</span>' for s in st.session_state.skills)
                st.markdown(f'<div class="card">{chips}</div>', unsafe_allow_html=True)
            else:
                st.write("No skills returned.")
        with col_b:
            st.markdown('<div class="section-title">Projects</div>', unsafe_allow_html=True)
            if st.session_state.projects:
                items = "".join(f"<li style='margin-bottom:4px;'>{p}</li>" for p in st.session_state.projects)
                st.markdown(f'<div class="card"><ul style="margin:0;padding-left:1.1rem;">{items}</ul></div>', unsafe_allow_html=True)
            else:
                st.write("No projects returned.")

# ---- Start ----------------------------------------------------------------
with tab_start:
    st.markdown('<div class="section-title">Start an interview</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="card">
        Mix: <b>{st.session_state.dsa_weight:.2f}</b> DSA / <b>{ai_ml_weight:.2f}</b> AI-ML
        &nbsp;-&nbsp; <span style="color:#94a3b8;">change it in the sidebar</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Start interview"):
        if not st.session_state.user_id:
            st.warning("Upload a resume or enter a User ID in the sidebar first.")
        else:
            payload = {
                "user_id": st.session_state.user_id,
                "domain_weights": {
                    "dsa": round(st.session_state.dsa_weight, 2),
                    "ai_ml": ai_ml_weight,
                },
            }
            with st.spinner("Preparing your first question..."):
                data, error = call_api("POST", "/start-session", json=payload)
            if error:
                st.error(error)
            else:
                st.session_state.session_id = data.get("session_id")
                st.session_state.question = normalize_question(data.get("first_question"))
                st.session_state.last_result = None
                st.session_state.answered = 0
                st.session_state.finished = False
                st.rerun()

    if st.session_state.session_id and st.session_state.question:
        st.success("Interview in progress - head to the Interview tab.")

# ---- Interview ------------------------------------------------------------
with tab_interview:
    st.markdown('<div class="section-title">Interview</div>', unsafe_allow_html=True)

    if st.session_state.last_result:
        show_result(st.session_state.last_result)
        st.divider()

    question = st.session_state.question

    if question:
        st.markdown('<div class="section-title">Current question</div>', unsafe_allow_html=True)
        show_question(question)

        # Keyed by question id so the box starts empty for every new question
        answer = st.text_area(
            "Your answer",
            height=220,
            placeholder="Type your answer here...",
            key=f"answer_{question['id']}",
        )

        if st.button("Submit answer"):
            if not answer.strip():
                st.warning("Please enter an answer first.")
            else:
                payload = {
                    "session_id": st.session_state.session_id,
                    "question_id": question["id"],
                    "answer": answer,
                }
                with st.spinner("Scoring your answer..."):
                    data, error = call_api("POST", "/submit-answer", json=payload)
                if error:
                    st.error(error)
                else:
                    st.session_state.last_result = data
                    st.session_state.answered += 1
                    st.session_state.question = normalize_question(data.get("next_question"))
                    st.session_state.finished = st.session_state.question is None
                    st.rerun()

    elif st.session_state.finished:
        st.success("That was the last question. Check the Progress tab for your summary.")
    else:
        st.info("Start an interview from the Start Interview tab first.")

# ---- Progress -------------------------------------------------------------
with tab_progress:
    st.markdown('<div class="section-title">Your progress</div>', unsafe_allow_html=True)

    if st.button("Load progress"):
        if not st.session_state.user_id:
            st.warning("Enter a User ID in the sidebar first.")
        else:
            data, error = call_api("GET", f"/progress/{st.session_state.user_id}")
            if error:
                st.error(error)
            else:
                left, right = st.columns(2)
                with left:
                    st.markdown('<div class="section-title">Weak topics</div>', unsafe_allow_html=True)
                    weak = data.get("weak_topics") or []
                    if weak:
                        chips = "".join(f'<span class="pill pill-hard" style="margin:3px;">{t}</span>' for t in weak)
                        st.markdown(f'<div class="card">{chips}</div>', unsafe_allow_html=True)
                    else:
                        st.write("None yet.")
                with right:
                    st.markdown('<div class="section-title">Strong topics</div>', unsafe_allow_html=True)
                    strong = data.get("strong_topics") or []
                    if strong:
                        chips = "".join(f'<span class="pill pill-easy" style="margin:3px;">{t}</span>' for t in strong)
                        st.markdown(f'<div class="card">{chips}</div>', unsafe_allow_html=True)
                    else:
                        st.write("None yet.")

                st.markdown('<div class="section-title">Recommended topics</div>', unsafe_allow_html=True)
                recs = data.get("recommended_topics") or {}
                if not recs:
                    st.write("No recommendations yet.")
                for topic, details in recs.items():
                    with st.container():
                        st.markdown(f"**{label(topic)}**")
                        # Backend may return either {"related": [...], "reason": "..."} or a plain list
                        if isinstance(details, dict):
                            related = details.get("related") or []
                            reason = details.get("reason")
                        else:
                            related = details or []
                            reason = None
                        if related:
                            st.write("Related: " + ", ".join(label(r) for r in related))
                        if reason:
                            st.caption(reason)

                st.markdown('<div class="section-title">Interview history</div>', unsafe_allow_html=True)
                history = data.get("history") or []
                if history:
                    df = pd.DataFrame(history)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    if len(df) > 1 and "avg_score" in df.columns:
                        x = df["date"] if "date" in df.columns else df.index
                        st.line_chart(df.set_index(x)["avg_score"])
                else:
                    st.write("No interview history yet.")
