import requests
import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Resume Interview AI",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_API_URL = "http://localhost:8000"
UPLOAD_FIELD_NAME = "file"
REQUEST_TIMEOUT = 120


# ============================================================
# PROFESSIONAL UI STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    .stApp {
        background: #f6f7fb;
        color: #172033;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    header {
        background: transparent !important;
    }

    /* Remove Streamlit decoration */
    [data-testid="stDecoration"] {
        display: none;
    }


    /* --------------------------------------------------------
       TYPOGRAPHY
    -------------------------------------------------------- */

    h1, h2, h3, h4 {
        color: #172033 !important;
        letter-spacing: -0.4px;
    }

    p {
        color: #667085;
    }


    /* --------------------------------------------------------
       HERO SECTION
    -------------------------------------------------------- */

    .hero {
        padding: 18px 0 32px 0;
    }

    .eyebrow {
        color: #635bff !important;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero-title {
        color: #111827 !important;
        font-size: 46px;
        line-height: 1.08;
        font-weight: 800;
        letter-spacing: -1.8px;
        margin: 0;
        max-width: 850px;
    }

    .hero-title .accent {
        color: #635bff !important;
    }

    .hero-description {
        color: #667085 !important;
        font-size: 17px;
        line-height: 1.7;
        max-width: 720px;
        margin-top: 18px;
    }


    /* --------------------------------------------------------
       SMALL STATUS BAR
    -------------------------------------------------------- */

    .status-bar {
        display: flex;
        align-items: center;
        gap: 9px;
        margin-top: 20px;
        color: #667085;
        font-size: 13px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
        display: inline-block;
    }


    /* --------------------------------------------------------
       SECTION LABEL
    -------------------------------------------------------- */

    .section-label {
        color: #344054 !important;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-top: 18px;
        margin-bottom: 12px;
    }


    /* --------------------------------------------------------
       FEATURE STRIP
    -------------------------------------------------------- */

    .feature-box {
        background: #ffffff;
        border: 1px solid #e6e8ef;
        border-radius: 14px;
        padding: 20px 22px;
        min-height: 125px;
        box-shadow: 0 4px 18px rgba(16, 24, 40, 0.04);
    }

    .feature-number {
        color: #635bff !important;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .feature-heading {
        color: #172033 !important;
        font-size: 17px;
        font-weight: 700;
        margin-top: 9px;
    }

    .feature-description {
        color: #667085 !important;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 5px;
    }


    /* --------------------------------------------------------
       UPLOAD AREA
    -------------------------------------------------------- */

    .upload-panel {
        background: #ffffff;
        border: 1px solid #e1e4eb;
        border-radius: 18px;
        padding: 30px;
        margin-top: 8px;
        margin-bottom: 25px;
        box-shadow: 0 8px 30px rgba(16, 24, 40, 0.05);
    }

    .upload-heading {
        color: #172033 !important;
        font-size: 22px;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .upload-description {
        color: #667085 !important;
        font-size: 14px;
        margin-bottom: 20px;
    }


    /* --------------------------------------------------------
       FILE UPLOADER
    -------------------------------------------------------- */

    [data-testid="stFileUploader"] {
        background: #fafbff;
        border: 1.5px dashed #c9c6ff;
        border-radius: 14px;
        padding: 8px;
    }

    [data-testid="stFileUploader"] section {
        background: transparent !important;
        border: none !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
    }


    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        border-radius: 9px;
        border: 1px solid #635bff;
        background: #635bff;
        color: #ffffff !important;
        font-weight: 650;
        font-size: 14px;
        min-height: 42px;
        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        background: #554de5;
        border-color: #554de5;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(99, 91, 255, 0.20);
    }


    /* --------------------------------------------------------
       TABS
    -------------------------------------------------------- */

    button[data-baseweb="tab"] {
        color: #667085 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding-left: 4px !important;
        padding-right: 4px !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #635bff !important;
    }

    [data-baseweb="tab-highlight"] {
        background-color: #635bff !important;
    }


    /* --------------------------------------------------------
       INFORMATION CARDS
    -------------------------------------------------------- */

    .info-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px 22px;
        margin: 10px 0;
    }

    .info-title {
        color: #172033 !important;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .info-text {
        color: #667085 !important;
        font-size: 14px;
        line-height: 1.6;
    }


    /* --------------------------------------------------------
       QUESTION CARD
    -------------------------------------------------------- */

    .question-card {
        background: #ffffff;
        border: 1px solid #e2e5ec;
        border-radius: 16px;
        padding: 26px;
        margin: 15px 0 22px 0;
        box-shadow: 0 7px 24px rgba(16, 24, 40, 0.05);
    }

    .question-label {
        color: #635bff !important;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }

    .question-main {
        color: #172033 !important;
        font-size: 21px;
        font-weight: 650;
        line-height: 1.5;
        margin-top: 12px;
    }

    .question-meta {
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #edf0f4;
        color: #667085 !important;
        font-size: 13px;
    }


    /* --------------------------------------------------------
       RESULT / SCORE
    -------------------------------------------------------- */

    .result-card {
        background: #ffffff;
        border: 1px solid #e2e5ec;
        border-radius: 16px;
        padding: 24px;
        margin: 15px 0 25px 0;
    }

    .result-label {
        color: #667085 !important;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .result-score {
        color: #635bff !important;
        font-size: 42px;
        font-weight: 800;
        line-height: 1;
        margin-top: 8px;
    }


    /* --------------------------------------------------------
       RESUME DETAILS
    -------------------------------------------------------- */

    .detail-card {
        background: #ffffff;
        border: 1px solid #e2e5ec;
        border-radius: 14px;
        padding: 20px;
        height: 100%;
    }

    .detail-heading {
        color: #172033 !important;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .tag {
        display: inline-block;
        background: #f1f0ff;
        color: #5148d9 !important;
        border: 1px solid #dedcff;
        border-radius: 6px;
        padding: 5px 9px;
        margin: 3px;
        font-size: 12px;
        font-weight: 600;
    }


    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    [data-testid="stSidebar"] {
        background: #171a24;
        border-right: 1px solid #292d3a;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #eef0f5 !important;
    }

    [data-testid="stSidebar"] input {
        background: #0f1117 !important;
        color: #ffffff !important;
        border: 1px solid #343847 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #343847 !important;
    }


    /* --------------------------------------------------------
       TEXT INPUTS
    -------------------------------------------------------- */

    textarea {
        border-radius: 10px !important;
        border: 1px solid #d9dde7 !important;
    }

    textarea:focus {
        border-color: #635bff !important;
        box-shadow: 0 0 0 1px #635bff !important;
    }


    /* --------------------------------------------------------
       METRICS
    -------------------------------------------------------- */

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e5ec;
        border-radius: 12px;
        padding: 15px;
    }


    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        margin-top: 70px;
        padding-top: 25px;
        border-top: 1px solid #e1e4eb;
        text-align: center;
        color: #98a2b3 !important;
        font-size: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
        "dsa_weight": 0.5,
        "answered": 0,
        "finished": False,
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


init_state()


# ============================================================
# HELPERS
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
        return (
            None,
            f"Cannot connect to the backend at "
            f"{st.session_state.api_url}. Is it running?"
        )

    except requests.exceptions.Timeout:
        return None, "The backend took too long to respond."

    except requests.exceptions.RequestException as exc:
        return None, f"Request failed: {exc}"

    if not response.ok:
        return (
            None,
            f"Backend returned {response.status_code}: "
            f"{response.text}"
        )

    try:
        return response.json(), None

    except ValueError:
        return None, "Backend did not return valid JSON."


def label(key):
    return key.replace("_", " ").title()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:20px;
            font-weight:750;
            color:#ffffff;
            margin-bottom:4px;
        ">
            Interview AI
        </div>

        <div style="
            font-size:12px;
            color:#98a2b3;
            margin-bottom:25px;
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
        help="Filled automatically after a resume upload."
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

    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            font-size:12px;
            color:#98a2b3;
            margin-top:5px;
        ">
            <span>DSA</span>
            <span>{st.session_state.dsa_weight:.2f}</span>
        </div>

        <div style="
            display:flex;
            justify-content:space-between;
            font-size:12px;
            color:#98a2b3;
            margin-top:5px;
        ">
            <span>AI / ML</span>
            <span>{ai_ml_weight:.2f}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.session_id:

        st.divider()

        st.markdown("### Current session")

        st.caption(
            f"Session: {st.session_state.session_id}"
        )

        st.write(
            f"Questions answered: "
            f"**{st.session_state.answered}**"
        )

        if st.button("End session"):

            st.session_state.session_id = None
            st.session_state.question = None
            st.session_state.last_result = None
            st.session_state.answered = 0
            st.session_state.finished = False

            st.rerun()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="eyebrow">
            RESUME INTELLIGENCE SYSTEM
        </div>

        <div class="hero-title">
            Turn your resume into
            <span class="accent">interview preparation.</span>
        </div>

        <div class="hero-description">
            Upload your resume and generate targeted DSA and
            AI/ML interview questions based on your skills,
            projects and experience.
        </div>

        <div class="status-bar">
            <span class="status-dot"></span>
            Interview generation system ready
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FEATURE STRIP
# ============================================================

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(
        """
        <div class="feature-box">
            <div class="feature-number">01</div>
            <div class="feature-heading">Resume Analysis</div>
            <div class="feature-description">
                Extract relevant skills and projects from
                your uploaded resume.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with f2:
    st.markdown(
        """
        <div class="feature-box">
            <div class="feature-number">02</div>
            <div class="feature-heading">Adaptive Questions</div>
            <div class="feature-description">
                Generate questions across DSA and AI/ML
                according to your selected domain mix.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with f3:
    st.markdown(
        """
        <div class="feature-box">
            <div class="feature-number">03</div>
            <div class="feature-heading">Answer Evaluation</div>
            <div class="feature-description">
                Submit answers and receive scoring,
                feedback and topic-level progress.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# NAVIGATION
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
        '<div class="section-label">Resume input</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="upload-panel">

            <div class="upload-heading">
                Upload your resume
            </div>

            <div class="upload-description">
                Upload a PDF resume to extract your skills,
                projects and interview-relevant information.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    pdf = st.file_uploader(
        "PDF resume",
        type=["pdf"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Analyse Resume",
        disabled=pdf is None,
        use_container_width=True
    ):

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

            st.rerun()


    # Resume results

    if (
        st.session_state.skills
        or st.session_state.projects
    ):

        st.markdown("<br>", unsafe_allow_html=True)

        st.success(
            "Resume successfully processed."
        )

        left, right = st.columns(2)

        with left:

            skills_html = ""

            for skill in st.session_state.skills:

                skills_html += (
                    f'<span class="tag">{skill}</span>'
                )

            if not skills_html:
                skills_html = (
                    '<span style="color:#667085">'
                    'No skills returned.'
                    '</span>'
                )

            st.markdown(
                f"""
                <div class="detail-card">

                    <div class="detail-heading">
                        Detected skills
                    </div>

                    {skills_html}

                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            projects_html = ""

            for project in st.session_state.projects:

                projects_html += (
                    f"""
                    <div style="
                        padding:8px 0;
                        color:#475467;
                        border-bottom:1px solid #eef0f4;
                    ">
                        {project}
                    </div>
                    """
                )

            if not projects_html:
                projects_html = (
                    '<span style="color:#667085">'
                    'No projects returned.'
                    '</span>'
                )

            st.markdown(
                f"""
                <div class="detail-card">

                    <div class="detail-heading">
                        Projects
                    </div>

                    {projects_html}

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# START INTERVIEW
# ============================================================

with tab_start:

    st.markdown(
        '<div class="section-label">Interview setup</div>',
        unsafe_allow_html=True
    )

    st.header("Start an interview")

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-title">
                Interview configuration
            </div>

            <div class="info-text">
                Questions will be generated using a
                <strong>{st.session_state.dsa_weight:.0%} DSA</strong>
                /
                <strong>{ai_ml_weight:.0%} AI/ML</strong>
                distribution.
                You can change this from the sidebar.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Start Interview",
        use_container_width=True
    ):

        if not st.session_state.user_id:

            st.warning(
                "Upload a resume or enter a User ID "
                "in the sidebar first."
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


    if (
        st.session_state.session_id
        and st.session_state.question
    ):

        st.success(
            "Interview ready. Open the Interview tab "
            "to answer your first question."
        )


# ============================================================
# INTERVIEW
# ============================================================

with tab_interview:

    st.markdown(
        '<div class="section-label">Live interview</div>',
        unsafe_allow_html=True
    )

    st.header("Interview")

    # Previous result

    if st.session_state.last_result:

        result = st.session_state.last_result

        breakdown = result.get(
            "breakdown"
        ) or {}

        st.markdown(
            """
            <div class="result-card">

                <div class="result-label">
                    Previous answer
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if breakdown:

            cols = st.columns(
                len(breakdown) + 1
            )

            cols[0].metric(
                "Score",
                result.get("score", "-")
            )

            for col, (key, value) in zip(
                cols[1:],
                breakdown.items()
            ):

                col.metric(
                    label(key),
                    value
                )

        else:

            st.metric(
                "Score",
                result.get("score", "-")
            )

        st.markdown(
            """
            <div class="info-card">

                <div class="info-title">
                    Feedback
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            result.get(
                "feedback"
            )
            or "No feedback available."
        )

        st.divider()


    question = st.session_state.question


    if question:

        st.markdown(
            f"""
            <div class="question-card">

                <div class="question-label">
                    Current question
                </div>

                <div class="question-main">
                    {question["question"]}
                </div>

                <div class="question-meta">
                    Topic: <strong>{question["topic"]}</strong>
                    &nbsp;&nbsp;·&nbsp;&nbsp;
                    Domain: <strong>{question["domain"]}</strong>
                    &nbsp;&nbsp;·&nbsp;&nbsp;
                    Difficulty: <strong>{question["difficulty"]}</strong>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        answer = st.text_area(
            "Your answer",
            height=220,
            placeholder=(
                "Write your answer as you would "
                "during an actual interview..."
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
                            data.get("next_question")
                        )
                    )

                    st.session_state.finished = (
                        st.session_state.question is None
                    )

                    st.rerun()


    elif st.session_state.finished:

        st.success(
            "Interview completed. "
            "Open Progress to review your performance."
        )

    else:

        st.info(
            "Start an interview from the Start Interview tab."
        )


# ============================================================
# PROGRESS
# ============================================================

with tab_progress:

    st.markdown(
        '<div class="section-label">Performance analytics</div>',
        unsafe_allow_html=True
    )

    st.header("Your progress")

    if st.button(
        "Load Progress",
        use_container_width=True
    ):

        if not st.session_state.user_id:

            st.warning(
                "Enter a User ID in the sidebar first."
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

                # Weak topics

                with left:

                    weak = (
                        data.get("weak_topics")
                        or []
                    )

                    st.markdown(
                        """
                        <div class="detail-card">

                            <div class="detail-heading">
                                Areas to improve
                            </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if weak:

                        for topic in weak:

                            st.markdown(
                                f"""
                                <div style="
                                    padding:9px 0;
                                    border-bottom:1px solid #eef0f4;
                                    color:#475467;
                                ">
                                    {topic}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:

                        st.write(
                            "No weak topics recorded yet."
                        )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


                # Strong topics

                with right:

                    strong = (
                        data.get("strong_topics")
                        or []
                    )

                    st.markdown(
                        """
                        <div class="detail-card">

                            <div class="detail-heading">
                                Strong areas
                            </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if strong:

                        for topic in strong:

                            st.markdown(
                                f"""
                                <div style="
                                    padding:9px 0;
                                    border-bottom:1px solid #eef0f4;
                                    color:#475467;
                                ">
                                    {topic}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:

                        st.write(
                            "No strong topics recorded yet."
                        )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


                # Recommendations

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown(
                    '<div class="section-label">Recommended topics</div>',
                    unsafe_allow_html=True
                )

                recs = (
                    data.get(
                        "recommended_topics"
                    )
                    or {}
                )

                if not recs:

                    st.info(
                        "No recommendations yet."
                    )

                else:

                    for topic, details in recs.items():

                        st.markdown(
                            f"""
                            <div class="info-card">

                                <div class="info-title">
                                    {label(topic)}
                                </div>
                            """,
                            unsafe_allow_html=True
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
                                    label(r)
                                    for r in related
                                )
                            )

                        if reason:

                            st.caption(reason)

                        st.markdown(
                            "</div>",
                            unsafe_allow_html=True
                        )


                # History

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown(
                    '<div class="section-label">Interview history</div>',
                    unsafe_allow_html=True
                )

                history = (
                    data.get("history")
                    or []
                )

                if history:

                    df = pd.DataFrame(history)

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

                        chart_df = df.set_index(x)[
                            ["avg_score"]
                        ]

                        st.line_chart(
                            chart_df,
                            use_container_width=True
                        )

                else:

                    st.info(
                        "No interview history yet."
                    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Resume Interview AI &nbsp;·&nbsp;
        Resume Analysis &nbsp;·&nbsp;
        DSA & AI/ML Interview Preparation
    </div>
    """,
    unsafe_allow_html=True
)
