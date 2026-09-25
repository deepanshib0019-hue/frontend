

import requests
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="InterviewAI",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ------------------------------
       GLOBAL
    ------------------------------ */

    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ------------------------------
       SIDEBAR
    ------------------------------ */

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #202938;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] input {
        background: #1f2937 !important;
        color: #f9fafb !important;
        border: 1px solid #374151 !important;
    }

    section[data-testid="stSidebar"] .stSlider > div > div {
        color: #ffffff;
    }

    /* ------------------------------
       HERO
    ------------------------------ */

    .hero {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #172554 100%
        );

        border-radius: 24px;
        padding: 42px 48px;
        margin-bottom: 28px;

        border: 1px solid #24324a;
        box-shadow: 0 15px 40px rgba(15, 23, 42, 0.12);
    }

    .eyebrow {
        color: #93c5fd;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 42px;
        font-weight: 750;
        line-height: 1.1;
        margin: 0;
    }

    .hero-title span {
        color: #60a5fa;
    }

    .hero-description {
        color: #cbd5e1;
        font-size: 16px;
        line-height: 1.7;
        max-width: 720px;
        margin-top: 16px;
    }

    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        margin-top: 22px;
        padding: 8px 14px;

        background: rgba(96, 165, 250, 0.10);
        border: 1px solid rgba(96, 165, 250, 0.25);
        border-radius: 999px;

        color: #bfdbfe;
        font-size: 13px;
        font-weight: 600;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background: #60a5fa;
        border-radius: 50%;
    }

    /* ------------------------------
       FEATURE CARDS
    ------------------------------ */

    .feature-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;

        padding: 25px;
        min-height: 155px;

        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);

        transition: transform 0.2s ease,
                    box-shadow 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
    }

    .feature-number {
        color: #2563eb;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 16px;
    }

    .feature-title {
        color: #111827;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    .feature-text {
        color: #64748b;
        font-size: 14px;
        line-height: 1.6;
    }

    /* ------------------------------
       SECTION HEADINGS
    ------------------------------ */

    .section-label {
        color: #64748b;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .section-title {
        color: #111827;
        font-size: 28px;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .section-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 22px;
    }

    /* ------------------------------
       UPLOAD CARD
    ------------------------------ */

    .upload-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 20px;

        padding: 30px;

        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);

        margin-top: 20px;
        margin-bottom: 28px;
    }

    .upload-title {
        color: #111827;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .upload-text {
        color: #64748b;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    /* ------------------------------
       BUTTONS
    ------------------------------ */

    .stButton > button {
        border-radius: 10px !important;
        border: 1px solid #2563eb !important;

        background: #2563eb !important;
        color: #ffffff !important;

        font-weight: 650 !important;

        padding: 10px 20px !important;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
    }

    /* ------------------------------
       TEXT AREA
    ------------------------------ */

    textarea {
        border-radius: 12px !important;
        border: 1px solid #dbe1ea !important;
    }

    /* ------------------------------
       METRICS
    ------------------------------ */

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 15px;
        padding: 18px;
    }

    /* ------------------------------
       TABS
    ------------------------------ */

    button[data-baseweb="tab"] {
        font-weight: 600;
        color: #64748b;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb;
    }

    /* ------------------------------
       QUESTION CARD
    ------------------------------ */

    .question-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #2563eb;

        border-radius: 16px;

        padding: 25px;

        margin: 18px 0;

        box-shadow: 0 7px 20px rgba(15, 23, 42, 0.05);
    }

    .question-label {
        color: #2563eb;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .question-text {
        color: #111827;
        font-size: 19px;
        font-weight: 650;
        line-height: 1.55;
    }

    /* ------------------------------
       INFO BOX
    ------------------------------ */

    .info-card {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 14px;
        padding: 18px;
        color: #1e3a8a;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_API_URL = "http://localhost:8000"
UPLOAD_FIELD_NAME = "file"
REQUEST_TIMEOUT = 120


# ============================================================
# SESSION STATE
# ============================================================

def init_state():

    defaults = {
        "api_url": DEFAULT_API_URL,
        "user_id": "",
        "session_id": None,
        "question": None,
        "last_result": None,
        "skills": [],
        "projects": [],
        "dsa_weight": 0.35,
        "answered": 0,
        "finished": False,
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


init_state()


# ============================================================
# API FUNCTIONS
# ============================================================

def normalize_question(q):

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

    url = f"{st.session_state.api_url.rstrip('/')}{path}"

    try:

        response = requests.request(
            method,
            url,
            timeout=REQUEST_TIMEOUT,
            **kwargs
        )

    except requests.exceptions.ConnectionError:

        return None, (
            f"Cannot connect to the backend at "
            f"{st.session_state.api_url}."
        )

    except requests.exceptions.Timeout:

        return None, "The backend took too long to respond."

    except requests.exceptions.RequestException as exc:

        return None, f"Request failed: {exc}"

    if not response.ok:

        return None, (
            f"Backend returned {response.status_code}: "
            f"{response.text}"
        )

    try:

        return response.json(), None

    except ValueError:

        return None, "Backend did not return valid JSON."


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:24px;
            font-weight:750;
            color:#ffffff;
            margin-bottom:4px;
        ">
            InterviewAI
        </div>

        <div style="
            font-size:13px;
            color:#94a3b8;
            margin-bottom:28px;
        ">
            Resume-driven interview preparation
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Configuration")

    st.text_input(
        "Backend URL",
        key="api_url"
    )

    st.text_input(
        "User ID",
        key="user_id",
        help="Automatically populated after resume upload."
    )

    st.divider()

    st.markdown("### Interview mix")

    st.slider(
        "DSA weight",
        0.0,
        1.0,
        step=0.05,
        key="dsa_weight"
    )

    ai_ml_weight = round(
        1.0 - st.session_state.dsa_weight,
        2
    )

    col1, col2 = st.columns(2)

    with col1:
        st.caption("DSA")
        st.write(f"**{st.session_state.dsa_weight:.2f}**")

    with col2:
        st.caption("AI / ML")
        st.write(f"**{ai_ml_weight:.2f}**")

    if st.session_state.session_id:

        st.divider()

        st.caption("CURRENT SESSION")

        st.write(
            f"Questions answered: "
            f"**{st.session_state.answered}**"
        )

        if st.button(
            "End session",
            use_container_width=True
        ):

            st.session_state.session_id = None
            st.session_state.question = None
            st.session_state.last_result = None
            st.session_state.answered = 0
            st.session_state.finished = False

            st.rerun()


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="eyebrow">
            AI INTERVIEW PREPARATION SYSTEM
        </div>

        <div class="hero-title">
            Turn your resume into
            <span>interview preparation.</span>
        </div>

        <div class="hero-description">
            Upload your resume and generate targeted DSA
            and AI/ML interview questions based on your
            skills, projects and experience.
        </div>

        <div class="status">
            <span class="status-dot"></span>
            Interview generation system ready
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FEATURE CARDS
# ============================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-number">01</div>

            <div class="feature-title">
                Resume Analysis
            </div>

            <div class="feature-text">
                Extract relevant skills and projects
                from your uploaded resume.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-number">02</div>

            <div class="feature-title">
                Adaptive Questions
            </div>

            <div class="feature-text">
                Generate questions across DSA and
                AI/ML according to your selected mix.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        """
        <div class="feature-card">

            <div class="feature-number">03</div>

            <div class="feature-title">
                Answer Evaluation
            </div>

            <div class="feature-text">
                Submit answers and receive scoring,
                feedback and topic-level progress.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# TABS
# ============================================================

tab_upload, tab_start, tab_interview, tab_progress = st.tabs(
    [
        "Resume",
        "Start Interview",
        "Interview",
        "Progress"
    ]
)


# ============================================================
# RESUME TAB
# ============================================================

with tab_upload:

    st.markdown(
        """
        <div class="section-label">
            RESUME INPUT
        </div>

        <div class="section-title">
            Upload your resume
        </div>

        <div class="section-description">
            Upload a PDF resume to extract skills, projects
            and interview-relevant information.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="upload-card">',
        unsafe_allow_html=True
    )

    pdf = st.file_uploader(
        "Choose your PDF resume",
        type=["pdf"],
        label_visibility="collapsed"
    )

    st.markdown(
        """
        <div class="upload-text">
            Supported format: PDF
        </div>
        """,
        unsafe_allow_html=True
    )

    upload_clicked = st.button(
        "Analyse Resume",
        disabled=pdf is None
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if upload_clicked:

        files = {
            UPLOAD_FIELD_NAME: (
                pdf.name,
                pdf.getvalue(),
                "application/pdf"
            )
        }

        with st.spinner("Analysing resume..."):

            data, error = call_api(
                "POST",
                "/upload-resume",
                files=files
            )

        if error:

            st.error(error)

        else:

            st.session_state.user_id = data.get(
                "user_id",
                st.session_state.user_id
            )

            st.session_state.skills = data.get(
                "skills",
                []
            )

            st.session_state.projects = data.get(
                "projects",
                []
            )

            weights = data.get(
                "domain_weights"
            ) or {}

            if "dsa" in weights:

                st.session_state.dsa_weight = float(
                    weights["dsa"]
                )

            st.success("Resume analysed successfully.")

            st.rerun()

    if (
        st.session_state.skills
        or st.session_state.projects
    ):

        st.markdown("### Resume analysis")

        left, right = st.columns(2)

        with left:

            st.markdown("**Detected skills**")

            if st.session_state.skills:

                st.write(
                    ", ".join(
                        st.session_state.skills
                    )
                )

            else:

                st.caption(
                    "No skills returned."
                )

        with right:

            st.markdown("**Projects**")

            if st.session_state.projects:

                for project in st.session_state.projects:

                    st.write(project)

            else:

                st.caption(
                    "No projects returned."
                )


# ============================================================
# START INTERVIEW TAB
# ============================================================

with tab_start:

    st.markdown(
        """
        <div class="section-label">
            INTERVIEW SETUP
        </div>

        <div class="section-title">
            Start your interview
        </div>

        <div class="section-description">
            Questions will be generated using the domain
            distribution selected in the sidebar.
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2 = st.columns(2)

    with m1:
        st.metric(
            "DSA",
            f"{st.session_state.dsa_weight:.0%}"
        )

    with m2:
        st.metric(
            "AI / ML",
            f"{ai_ml_weight:.0%}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Start Interview",
        use_container_width=True
    ):

        if not st.session_state.user_id:

            st.warning(
                "Upload a resume or enter a User ID first."
            )

        else:

            payload = {
                "user_id": st.session_state.user_id,
                "domain_weights": {
                    "dsa": round(
                        st.session_state.dsa_weight,
                        2
                    ),
                    "ai_ml": ai_ml_weight,
                },
            }

            with st.spinner(
                "Preparing your first question..."
            ):

                data, error = call_api(
                    "POST",
                    "/start-session",
                    json=payload
                )

            if error:

                st.error(error)

            else:

                st.session_state.session_id = (
                    data.get("session_id")
                )

                st.session_state.question = (
                    normalize_question(
                        data.get("first_question")
                    )
                )

                st.session_state.last_result = None
                st.session_state.answered = 0
                st.session_state.finished = False

                st.rerun()


# ============================================================
# INTERVIEW TAB
# ============================================================

with tab_interview:

    st.markdown(
        """
        <div class="section-label">
            LIVE INTERVIEW
        </div>

        <div class="section-title">
            Practice your answer
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.last_result:

        result = st.session_state.last_result

        st.markdown("### Previous answer")

        score = result.get(
            "score",
            "-"
        )

        domain = result.get(
            "domain",
            ""
        )

        a, b = st.columns(2)

        with a:
            st.metric("Score", score)

        with b:
            st.metric("Domain", domain)

        breakdown = result.get(
            "breakdown"
        ) or {}

        if breakdown:

            cols = st.columns(
                len(breakdown)
            )

            for col, (key, value) in zip(
                cols,
                breakdown.items()
            ):

                with col:

                    st.metric(
                        key.replace(
                            "_",
                            " "
                        ).title(),
                        value
                    )

        st.markdown("**Feedback**")

        st.write(
            result.get(
                "feedback",
                "No feedback available."
            )
        )

        st.divider()

    question = st.session_state.question

    if question:

        st.markdown(
            f"""
            <div class="question-card">

                <div class="question-label">
                    CURRENT QUESTION
                </div>

                <div class="question-text">
                    {question["question"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        q1, q2, q3 = st.columns(3)

        with q1:
            st.caption("TOPIC")
            st.write(
                question["topic"]
            )

        with q2:
            st.caption("DOMAIN")
            st.write(
                question["domain"]
            )

        with q3:
            st.caption("DIFFICULTY")
            st.write(
                question["difficulty"]
            )

        answer = st.text_area(
            "Your answer",
            height=220,
            placeholder=(
                "Explain your approach, reasoning "
                "and solution here..."
            ),
            key=f"answer_{question['id']}"
        )

        if st.button(
            "Submit Answer",
            use_container_width=True
        ):

            if not answer.strip():

                st.warning(
                    "Please enter an answer first."
                )

            else:

                payload = {
                    "session_id":
                        st.session_state.session_id,

                    "question_id":
                        question["id"],

                    "answer":
                        answer,
                }

                with st.spinner(
                    "Evaluating your answer..."
                ):

                    data, error = call_api(
                        "POST",
                        "/submit-answer",
                        json=payload
                    )

                if error:

                    st.error(error)

                else:

                    st.session_state.last_result = data

                    st.session_state.answered += 1

                    st.session_state.question = (
                        normalize_question(
                            data.get(
                                "next_question"
                            )
                        )
                    )

                    st.session_state.finished = (
                        st.session_state.question
                        is None
                    )

                    st.rerun()

    elif st.session_state.finished:

        st.success(
            "Interview completed. "
            "Open Progress to view your summary."
        )

    else:

        st.markdown(
            """
            <div class="info-card">
                Start an interview from the
                <strong>Start Interview</strong> tab
                to receive your first question.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# PROGRESS TAB
# ============================================================

with tab_progress:

    st.markdown(
        """
        <div class="section-label">
            PERFORMANCE
        </div>

        <div class="section-title">
            Your progress
        </div>

        <div class="section-description">
            Review your interview performance and
            identify topics that need more practice.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Load Progress",
        use_container_width=True
    ):

        if not st.session_state.user_id:

            st.warning(
                "Enter a User ID first."
            )

        else:

            data, error = call_api(
                "GET",
                f"/progress/{st.session_state.user_id}"
            )

            if error:

                st.error(error)

            else:

                left, right = st.columns(2)

                weak = data.get(
                    "weak_topics"
                ) or []

                strong = data.get(
                    "strong_topics"
                ) or []

                with left:

                    st.markdown("### Areas to improve")

                    if weak:

                        for topic in weak:
                            st.write(topic)

                    else:

                        st.caption(
                            "No weak topics identified yet."
                        )

                with right:

                    st.markdown("### Strong topics")

                    if strong:

                        for topic in strong:
                            st.write(topic)

                    else:

                        st.caption(
                            "No strong topics identified yet."
                        )

                st.divider()

                st.markdown(
                    "### Recommended topics"
                )

                recommendations = data.get(
                    "recommended_topics"
                ) or {}

                if recommendations:

                    for topic, details in recommendations.items():

                        st.markdown(
                            f"**{topic.replace('_', ' ').title()}**"
                        )

                        if isinstance(
                            details,
                            dict
                        ):

                            related = (
                                details.get(
                                    "related"
                                )
                                or []
                            )

                            reason = details.get(
                                "reason"
                            )

                        else:

                            related = (
                                details
                                or []
                            )

                            reason = None

                        if related:

                            st.write(
                                "Related: "
                                + ", ".join(
                                    related
                                )
                            )

                        if reason:

                            st.caption(
                                reason
                            )

                else:

                    st.caption(
                        "No recommendations yet."
                    )

                st.divider()

                st.markdown(
                    "### Interview history"
                )

                history = data.get(
                    "history"
                ) or []

                if history:

                    df = pd.DataFrame(
                        history
                    )

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )

                    if (
                        len(df) > 1
                        and "avg_score" in df.columns
                    ):

                        x = (
                            df["date"]
                            if "date" in df.columns
                            else df.index
                        )

                        chart_df = df.set_index(x)

                        st.line_chart(
                            chart_df[
                                ["avg_score"]
                            ]
                        )

                else:

                    st.caption(
                        "No interview history yet."
                    )
