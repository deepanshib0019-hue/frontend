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
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f6f8fc;
}

/* Remove default top spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1250px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white;
}

/* Main hero */
.hero {
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1e293b 55%,
        #334155 100%
    );

    padding: 55px 55px 50px 55px;
    border-radius: 24px;
    margin-bottom: 30px;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.14);
}

.hero-label {
    color: #93c5fd;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.hero-title {
    color: white;
    font-size: 46px;
    line-height: 1.1;
    font-weight: 800;
    margin: 0;
}

.hero-title span {
    color: #60a5fa;
}

.hero-description {
    color: #cbd5e1;
    font-size: 17px;
    line-height: 1.7;
    max-width: 720px;
    margin-top: 20px;
}

.status {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-top: 28px;
    padding: 9px 15px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 30px;
    color: #dbeafe;
    font-size: 13px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
}


/* Feature cards */

.feature-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 25px;
    min-height: 155px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

.feature-number {
    color: #2563eb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 15px;
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


/* Section headings */

.section-label {
    color: #2563eb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.section-title {
    color: #111827;
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 8px;
}

.section-description {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 25px;
}


/* Upload area */

.upload-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 30px rgba(15,23,42,0.05);
    margin-top: 20px;
}

.upload-title {
    color: #111827;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 8px;
}

.upload-description {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 20px;
}


/* Metrics */

.metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 6px 20px rgba(15,23,42,0.04);
}

.metric-label {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 6px;
}

.metric-value {
    color: #111827;
    font-size: 28px;
    font-weight: 800;
}


/* Question card */

.question-card {
    background: white;
    border: 1px solid #dbeafe;
    border-left: 4px solid #2563eb;
    border-radius: 18px;
    padding: 28px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

.question-label {
    color: #2563eb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.question-text {
    color: #111827;
    font-size: 21px;
    line-height: 1.55;
    font-weight: 600;
    margin-top: 12px;
}


/* Tags */

.tag {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #dbeafe;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 7px;
}


/* Buttons */

.stButton > button {
    width: 100%;
    min-height: 45px;
    border-radius: 10px;
    border: 1px solid #2563eb;
    background: #2563eb;
    color: white;
    font-weight: 600;
    font-size: 14px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #1d4ed8;
    border-color: #1d4ed8;
}


/* File uploader */

[data-testid="stFileUploader"] {
    background: #f8fafc;
    border: 1px dashed #94a3b8;
    border-radius: 14px;
    padding: 10px;
}


/* Text area */

textarea {
    border-radius: 12px !important;
}


/* Tabs */

button[data-baseweb="tab"] {
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563eb;
}


/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
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
        "dsa_weight": 0.5,
        "answered": 0,
        "finished": False,
        "progress_data": None,
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
# DISPLAY FUNCTIONS
# ============================================================

def show_question(q):

    st.markdown(
        f"""
        <div class="question-card">

            <div class="question-label">
                Current Interview Question
            </div>

            <div class="question-text">
                {q["question"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f'<span class="tag">Topic: {q["topic"]}</span>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f'<span class="tag">Domain: {q["domain"]}</span>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f'<span class="tag">Difficulty: {q["difficulty"]}</span>',
            unsafe_allow_html=True
        )


def show_result(result):

    st.markdown(
        """
        <div class="section-label">
            Evaluation
        </div>

        <div class="section-title">
            Answer analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    score = result.get("score", "-")
    domain = result.get("domain", "-")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Overall Score
                </div>

                <div class="metric-value">
                    {score}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Domain
                </div>

                <div class="metric-value"
                     style="font-size:22px;">
                    {domain}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    breakdown = result.get("breakdown") or {}

    if breakdown:

        st.write("")

        cols = st.columns(len(breakdown))

        for col, (key, value) in zip(cols, breakdown.items()):

            with col:
                st.metric(
                    key.replace("_", " ").title(),
                    value
                )

    st.write("")

    st.markdown(
        '<div class="section-label">Feedback</div>',
        unsafe_allow_html=True
    )

    feedback = result.get("feedback")

    if feedback:

        st.info(feedback)

    else:

        st.write("No feedback available.")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:26px;
            font-weight:800;
            color:white;
            margin-bottom:4px;
        ">
            InterviewAI
        </div>

        <div style="
            color:#94a3b8;
            font-size:13px;
            margin-bottom:35px;
        ">
            Resume-driven interview preparation
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### Configuration"
    )

    st.text_input(
        "Backend URL",
        key="api_url"
    )

    st.text_input(
        "User ID",
        key="user_id",
        help="Automatically filled after resume upload."
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

    st.write(
        f"DSA: **{st.session_state.dsa_weight:.2f}**"
    )

    st.write(
        f"AI / ML: **{ai_ml_weight:.2f}**"
    )

    if st.session_state.session_id:

        st.divider()

        st.markdown("### Current session")

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
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-label">
            RESUME INTELLIGENCE SYSTEM
        </div>

        <div class="hero-title">
            Turn your resume into
            <span>interview preparation.</span>
        </div>

        <div class="hero-description">
            Upload your resume and generate targeted
            DSA and AI/ML interview questions based on
            your skills, projects and experience.
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

            <div class="feature-number">
                01
            </div>

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

            <div class="feature-number">
                02
            </div>

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

            <div class="feature-number">
                03
            </div>

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


st.write("")
st.write("")


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
        """
        <div class="section-label">
            RESUME INPUT
        </div>

        <div class="section-title">
            Upload your resume
        </div>

        <div class="section-description">
            Upload a PDF resume to extract your skills,
            projects and interview-relevant information.
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
        type=["pdf"]
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "Analyse Resume",
        disabled=pdf is None
    ):

        files = {
            UPLOAD_FIELD_NAME: (
                pdf.name,
                pdf.getvalue(),
                "application/pdf"
            )
        }

        with st.spinner(
            "Analysing resume..."
        ):

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

            st.success(
                "Resume analysed successfully."
            )

            st.rerun()


    if (
        st.session_state.skills
        or st.session_state.projects
    ):

        st.write("")

        st.markdown(
            """
            <div class="section-label">
                RESUME ANALYSIS
            </div>

            <div class="section-title">
                Extracted profile
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                '<div class="metric-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="metric-label">Skills detected</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="metric-value">{len(st.session_state.skills)}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                '<div class="metric-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="metric-label">Projects detected</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="metric-value">{len(st.session_state.projects)}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        st.write("")

        if st.session_state.skills:

            st.subheader("Detected skills")

            for skill in st.session_state.skills:

                st.markdown(
                    f'<span class="tag">{skill}</span>',
                    unsafe_allow_html=True
                )

        if st.session_state.projects:

            st.write("")

            st.subheader("Projects")

            for project in st.session_state.projects:

                st.write(
                    f"• {project}"
                )


# ============================================================
# START INTERVIEW
# ============================================================

with tab_start:

    st.markdown(
        """
        <div class="section-label">
            INTERVIEW SETUP
        </div>

        <div class="section-title">
            Start an adaptive interview
        </div>

        <div class="section-description">
            Configure the interview domain mix and
            generate your first personalised question.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    DSA questions
                </div>

                <div class="metric-value">
                    {st.session_state.dsa_weight:.0%}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    AI / ML questions
                </div>

                <div class="metric-value">
                    {ai_ml_weight:.0%}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    if st.button("Start Interview"):

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
                    "ai_ml": ai_ml_weight
                }
            }

            with st.spinner(
                "Preparing your interview..."
            ):

                data, error = call_api(
                    "POST",
                    "/start-session",
                    json=payload
                )

            if error:

                st.error(error)

            else:

                st.session_state.session_id = data.get(
                    "session_id"
                )

                st.session_state.question = normalize_question(
                    data.get("first_question")
                )

                st.session_state.last_result = None
                st.session_state.answered = 0
                st.session_state.finished = False

                st.success(
                    "Interview session created."
                )

                st.rerun()

    if (
        st.session_state.session_id
        and st.session_state.question
    ):

        st.info(
            "Your interview is ready. Open the Interview tab."
        )


# ============================================================
# INTERVIEW
# ============================================================

with tab_interview:

    st.markdown(
        """
        <div class="section-label">
            LIVE INTERVIEW
        </div>

        <div class="section-title">
            Practice and evaluate
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.last_result:

        show_result(
            st.session_state.last_result
        )

        st.divider()

    question = st.session_state.question

    if question:

        show_question(question)

        answer = st.text_area(
            "Your answer",
            height=230,
            placeholder=(
                "Write your answer as you would "
                "during a technical interview..."
            ),
            key=f"answer_{question['id']}"
        )

        if st.button("Submit Answer"):

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
                        answer
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

                    st.session_state.question = normalize_question(
                        data.get("next_question")
                    )

                    st.session_state.finished = (
                        st.session_state.question is None
                    )

                    st.rerun()

    elif st.session_state.finished:

        st.success(
            "Interview completed. "
            "Open Progress to view your summary."
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
        """
        <div class="section-label">
            PERFORMANCE
        </div>

        <div class="section-title">
            Track your progress
        </div>

        <div class="section-description">
            Review weak topics, strong topics and
            recommended areas for further practice.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Load Progress"):

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

                st.session_state.progress_data = data


    data = st.session_state.progress_data

    if data:

        weak = data.get(
            "weak_topics"
        ) or []

        strong = data.get(
            "strong_topics"
        ) or []

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                """
                <div class="metric-card">

                    <div class="metric-label">
                        Weak topics
                    </div>

                    <div class="metric-value">
                        %d
                    </div>

                </div>
                """ % len(weak),
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                """
                <div class="metric-card">

                    <div class="metric-label">
                        Strong topics
                    </div>

                    <div class="metric-value">
                        %d
                    </div>

                </div>
                """ % len(strong),
                unsafe_allow_html=True
            )

        st.write("")

        left, right = st.columns(2)

        with left:

            st.subheader("Weak topics")

            if weak:

                for topic in weak:

                    st.markdown(
                        f'<span class="tag">{topic}</span>',
                        unsafe_allow_html=True
                    )

            else:

                st.write(
                    "No weak topics identified yet."
                )

        with right:

            st.subheader("Strong topics")

            if strong:

                for topic in strong:

                    st.markdown(
                        f'<span class="tag">{topic}</span>',
                        unsafe_allow_html=True
                    )

            else:

                st.write(
                    "No strong topics identified yet."
                )


        st.write("")

        st.subheader(
            "Recommended topics"
        )

        recs = data.get(
            "recommended_topics"
        ) or {}

        if recs:

            for topic, details in recs.items():

                st.markdown(
                    f"**{topic.replace('_', ' ').title()}**"
                )

                if isinstance(details, dict):

                    related = details.get(
                        "related"
                    ) or []

                    reason = details.get(
                        "reason"
                    )

                else:

                    related = details or []
                    reason = None

                if related:

                    st.write(
                        "Related: "
                        + ", ".join(
                            r.replace("_", " ").title()
                            for r in related
                        )
                    )

                if reason:

                    st.caption(
                        reason
                    )

        else:

            st.write(
                "No recommendations available yet."
            )


        st.write("")

        st.subheader(
            "Interview history"
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

                chart_df = df.set_index(x)[
                    ["avg_score"]
                ]

                st.line_chart(
                    chart_df
                )

        else:

            st.write(
                "No interview history available yet."
            )
