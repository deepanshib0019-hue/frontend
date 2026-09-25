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
# Conimport streamlit as st

st.set_page_config(
    page_title="InterviewAI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f8f9ff 0%, #eef1ff 100%);
    }

    /* Remove top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Main title */
    .hero-title {
        font-size: 55px;
        font-weight: 800;
        text-align: center;
        color: #15162b;
        margin-bottom: 10px;
    }

    .hero-title span {
        color: #6c63ff;
    }

    /* Subtitle */
    .hero-subtitle {
        text-align: center;
        font-size: 19px;
        color: #666b85;
        margin-bottom: 35px;
    }

    /* Feature cards */
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        border: 1px solid #eeeeff;
        height: 160px;
    }

    .feature-icon {
        font-size: 35px;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 700;
        color: #20213a;
    }

    .feature-text {
        font-size: 14px;
        color: #777b91;
    }

    /* Upload section */
    .upload-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.07);
        margin-top: 25px;
        margin-bottom: 35px;
    }

    /* Question cards */
    .question-card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        margin: 15px 0;
        border-left: 5px solid #6c63ff;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }

    .question-number {
        color: #6c63ff;
        font-weight: 800;
        font-size: 14px;
    }

    .question-text {
        color: #20213a;
        font-size: 17px;
        font-weight: 600;
        margin-top: 8px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 12px;
        font-size: 16px;
        font-weight: 700;
        background: #6c63ff;
        color: white;
    }

    .stButton > button:hover {
        background: #554be8;
        color: white;
    }

</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------------------------------
DEFAULT_API_URL = "http://localhost:8000"
UPLOAD_FIELD_NAME = "file"   # multipart field name for the PDF in POST /upload-resume
REQUEST_TIMEOUT = 120        # seconds; scoring by an LLM can be slow

st.set_page_config(page_title="Resume Interview Generator", page_icon="🎯", layout="wide")


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


def show_question(q):
    st.info(q["question"])
    c1, c2, c3 = st.columns(3)
    c1.write(f"**Topic:** {q['topic']}")
    c2.write(f"**Domain:** {q['domain']}")
    c3.write(f"**Difficulty:** {q['difficulty']}")


def show_result(result):
    st.subheader("Result of your last answer")
    top1, top2 = st.columns([1, 3])
    top1.metric("Score", result.get("score", "-"))
    top2.write(f"**Domain:** {result.get('domain', '')}")

    breakdown = result.get("breakdown") or {}
    if breakdown:
        cols = st.columns(len(breakdown))
        for col, (key, value) in zip(cols, breakdown.items()):
            col.metric(label(key), value)

    st.write("**Feedback**")
    st.write(result.get("feedback") or "No feedback available.")


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
init_state()

st.sidebar.header("Settings")
st.session_state.setdefault("api_url", DEFAULT_API_URL)
st.sidebar.text_input("Backend URL", key="api_url")

st.sidebar.text_input(
    "User ID",
    key="user_id",
    help="Filled automatically after a resume upload. Enter an existing ID to continue as a returning user.",
)

st.sidebar.divider()
st.sidebar.subheader("Domain mix")
st.sidebar.slider("DSA weight", 0.0, 1.0, step=0.05, key="dsa_weight")
ai_ml_weight = round(1.0 - st.session_state.dsa_weight, 2)
st.sidebar.write(f"AI/ML weight: **{ai_ml_weight:.2f}**")

if st.session_state.session_id:
    st.sidebar.divider()
    st.sidebar.write(f"Session: `{st.session_state.session_id}`")
    st.sidebar.write(f"Questions answered: **{st.session_state.answered}**")
    if st.sidebar.button("End session"):
        st.session_state.session_id = None
        st.session_state.question = None
        st.session_state.last_result = None
        st.session_state.answered = 0
        st.session_state.finished = False
        st.rerun()


# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------
st.title("🎯 Resume-to-Interview Questions Generator")
st.caption("Upload your resume, then practice DSA and AI/ML interview questions.")

tab_upload, tab_start, tab_interview, tab_progress = st.tabs(
    ["📄 Upload Resume", "🚀 Start Interview", "💬 Interview", "📊 Progress"]
)

# ---- Upload ---------------------------------------------------------------
with tab_upload:
    st.header("Upload your resume")
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
        st.subheader("Detected skills")
        st.write(", ".join(st.session_state.skills) or "No skills returned.")
        st.subheader("Projects")
        if st.session_state.projects:
            for project in st.session_state.projects:
                st.write(f"• {project}")
        else:
            st.write("No projects returned.")

# ---- Start ----------------------------------------------------------------
with tab_start:
    st.header("Start an interview")
    st.write(
        f"Mix: **{st.session_state.dsa_weight:.2f}** DSA / **{ai_ml_weight:.2f}** AI/ML "
        "(change it in the sidebar)."
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
        st.success("Interview in progress - head to the **Interview** tab.")

# ---- Interview ------------------------------------------------------------
with tab_interview:
    st.header("Interview")

    if st.session_state.last_result:
        show_result(st.session_state.last_result)
        st.divider()

    question = st.session_state.question

    if question:
        st.subheader("Current question")
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
        st.success("That was the last question. Check the **Progress** tab for your summary.")
    else:
        st.info("Start an interview from the **Start Interview** tab first.")

# ---- Progress -------------------------------------------------------------
with tab_progress:
    st.header("Your progress")

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
                    st.subheader("🔴 Weak topics")
                    weak = data.get("weak_topics") or []
                    for t in weak:
                        st.write(f"• {t}")
                    if not weak:
                        st.write("None yet.")
                with right:
                    st.subheader("🟢 Strong topics")
                    strong = data.get("strong_topics") or []
                    for t in strong:
                        st.write(f"• {t}")
                    if not strong:
                        st.write("None yet.")

                st.subheader("📚 Recommended topics")
                recs = data.get("recommended_topics") or {}
                if not recs:
                    st.write("No recommendations yet.")
                for topic, details in recs.items():
                    st.write(f"**{label(topic)}**")
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

                st.subheader("📜 Interview history")
                history = data.get("history") or []
                if history:
                    df = pd.DataFrame(history)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    if len(df) > 1 and "avg_score" in df.columns:
                        x = df["date"] if "date" in df.columns else df.index
                        st.line_chart(df.set_index(x)["avg_score"])
                else:
                    st.write("No interview history yet.")
