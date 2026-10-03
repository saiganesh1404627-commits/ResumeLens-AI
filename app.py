import streamlit as st
from pypdf import PdfReader
from google import genai

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ResumeLens AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PROFESSIONAL UI
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #050505;
    --panel: #0b0b0b;
    --panel-2: #111111;
    --line: #292929;
    --line-strong: #3a3a3a;
    --text: #f5f5f5;
    --muted: #a3a3a3;
    --muted-2: #777777;
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

.main .block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Make every important piece of text readable on black */
h1, h2, h3, h4, h5, h6,
p, li, label, .stMarkdown, .stCaption,
[data-testid="stCaptionContainer"],
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: var(--text) !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

h1 {
    font-size: clamp(2.4rem, 5vw, 4rem) !important;
    line-height: 1.02 !important;
    margin-bottom: 0.4rem !important;
}

h2 { font-size: 1.7rem !important; }
h3 { font-size: 1.2rem !important; }

/* Hero */
.hero {
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 2.1rem 2.3rem;
    margin-bottom: 1.2rem;
    background: var(--panel);
}

.eyebrow {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #bdbdbd !important;
    margin-bottom: 0.7rem;
}

.hero-subtitle {
    font-size: 1rem;
    line-height: 1.7;
    color: #b8b8b8 !important;
    max-width: 780px;
}

.feature-pill {
    display: inline-block;
    border: 1px solid var(--line-strong);
    border-radius: 999px;
    padding: 0.34rem 0.7rem;
    margin: 0.25rem 0.25rem 0 0;
    font-size: 0.76rem;
    color: #d8d8d8 !important;
    background: var(--panel-2);
}

.section-note {
    color: #a5a5a5 !important;
    font-size: 0.9rem;
    margin-top: -0.3rem;
    margin-bottom: 1rem;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background: #080808 !important;
    color: var(--text) !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: var(--text) !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #0d0d0d !important;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background: #0b0b0b !important;
    color: #f5f5f5 !important;
    caret-color: #ffffff !important;
    border: 1px solid #353535 !important;
    border-radius: 11px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-baseweb="input"] input::placeholder,
[data-baseweb="textarea"] textarea::placeholder {
    color: #707070 !important;
    opacity: 1 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
[data-baseweb="input"] input:focus,
[data-baseweb="textarea"] textarea:focus {
    border-color: #666666 !important;
    box-shadow: 0 0 0 1px #666666 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #0b0b0b !important;
    border: 1px dashed #444444 !important;
    border-radius: 13px !important;
}

[data-testid="stFileUploader"] * {
    color: #eeeeee !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #9b9b9b !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    min-height: 45px;
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 10px !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background: #1b1b1b !important;
    color: #ffffff !important;
    border-color: #686868 !important;
}

/* Tabs - simple and understandable */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.2rem;
    background: #080808;
    border-bottom: 1px solid #292929;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    padding: 0 1rem;
    color: #858585 !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab"] p {
    color: inherit !important;
}

.stTabs [aria-selected="true"] {
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: #ffffff !important;
}

/* Cards and metrics */
.result-card,
.status,
div[data-testid="stMetric"] {
    background: var(--panel) !important;
    border: 1px solid var(--line) !important;
    color: var(--text) !important;
}

.result-card {
    border-radius: 14px;
    padding: 1.15rem 1.3rem;
    margin: 0.7rem 0 1rem 0;
}

.result-card strong {
    color: #ffffff !important;
}

.status {
    border-radius: 10px;
    padding: 0.65rem 0.8rem;
    font-size: 0.88rem;
}

div[data-testid="stMetric"] {
    border-radius: 13px;
    padding: 0.9rem;
}

/* Alerts */
[data-testid="stAlert"] {
    background: #101010 !important;
    color: #f2f2f2 !important;
    border: 1px solid #303030 !important;
    border-radius: 11px !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #f2f2f2 !important;
}

/* Expanders / dropdowns */
[data-testid="stExpander"],
[data-baseweb="select"] > div,
[data-baseweb="popover"] > div {
    background: #0b0b0b !important;
    color: #f5f5f5 !important;
    border-color: #333333 !important;
}

/* Dividers */
hr {
    border-color: #282828 !important;
}

/* Footer */
.footer {
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid #282828;
    text-align: center;
    color: #777777 !important;
    font-size: 0.82rem;
}

.footer strong {
    color: #eeeeee !important;
}

.footer span {
    color: #666666 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# GEMINI CONNECTION
# ============================================================

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Gemini API setup is missing. Add GEMINI_API_KEY to .streamlit/secrets.toml.")
    st.stop()

MODEL_NAME = "gemini-2.5-flash"

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "resume_text": "",
    "resume_name": "",
    "analysis_result": "",
    "match_result": "",
    "bullet_result": "",
    "project_result": "",
    "interview_result": "",
    "mock_history": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# HELPERS
# ============================================================

def generate_ai(prompt):
    """Send a prompt to Gemini and return clean text."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()


def require_resume():
    if not st.session_state.resume_text.strip():
        st.warning("Upload a readable PDF resume from the sidebar first.")
        return False
    return True


def result_box(title, content):
    st.markdown(
        f'<div class="result-card"><strong>{title}</strong></div>',
        unsafe_allow_html=True
    )
    st.markdown(content)


# ============================================================
# SIDEBAR — RESUME WORKSPACE
# ============================================================

with st.sidebar:
    st.markdown("## ResumeLens AI")
    st.caption("Your private resume workspace")

    st.markdown("### 01 · Upload")
    resume = st.file_uploader(
        "Choose your resume",
        type=["pdf"],
        help="Use a text-based PDF for the best extraction quality.",
    )

    if resume is not None:
        if resume.name != st.session_state.resume_name:
            st.session_state.resume_name = resume.name
            st.session_state.resume_text = ""
            st.session_state.analysis_result = ""
            st.session_state.match_result = ""
            st.session_state.project_result = ""
            st.session_state.interview_result = ""
            st.session_state.mock_history = []

            try:
                reader = PdfReader(resume)
                extracted = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted.append(page_text)

                st.session_state.resume_text = "\n\n".join(extracted).strip()

            except Exception as e:
                st.error(f"Could not read the PDF: {e}")
                st.session_state.resume_text = ""

        if st.session_state.resume_text.strip():
            st.success(f"Ready: {resume.name}")
            st.caption(
                f"{len(st.session_state.resume_text):,} characters extracted"
            )
        else:
            st.warning(
                "No readable text was found. Try a text-based PDF instead of a scanned image PDF."
            )

    st.divider()

    st.markdown("### 02 · Workspace")
    if st.session_state.resume_text.strip():
        st.markdown(
            '<div class="status">✓ Resume loaded and available across all tools.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status">○ Upload a resume to unlock the tools.</div>',
            unsafe_allow_html=True
        )

    st.divider()
    st.caption("PDF only • Powered by Gemini")
    st.caption("Built for students, freshers & early-career professionals")

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">AI Career Workspace</div>
    <h1>ResumeLens AI</h1>
    <div class="hero-subtitle">
        Turn your resume into clear career insights, job-match analysis,
        stronger resume content, portfolio ideas, and interview practice.
    </div>
    <div style="margin-top: 1rem;">
        <span class="feature-pill">Resume Analysis</span>
        <span class="feature-pill">Job Matching</span>
        <span class="feature-pill">Resume Tools</span>
        <span class="feature-pill">Project Ideas</span>
        <span class="feature-pill">Interview Practice</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MAIN NAVIGATION
# ============================================================

resume_tab, match_tab, tools_tab, projects_tab, interview_tab = st.tabs([
    "📄 Resume",
    "🎯 Job Match",
    "✍️ Resume Tools",
    "💼 Projects",
    "🎤 Interview",
])

# ============================================================
# TAB 1 — RESUME ANALYSIS
# ============================================================

with resume_tab:
    st.header("Resume Analysis")
    st.markdown(
        '<div class="section-note">Understand what your resume communicates before you apply.</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.resume_text.strip():
        st.info("Upload your PDF resume from the sidebar to begin.")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f'<div class="status">✓ <strong>{st.session_state.resume_name}</strong> is ready for analysis.</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.metric("Resume text", f"{len(st.session_state.resume_text):,} chars")

        st.write("")
        if st.button("Analyze My Resume", use_container_width=True, key="analyze_resume"):
            prompt = f"""
You are ResumeLens AI, a professional resume analysis assistant.

Analyze the following resume.

RESUME:
{st.session_state.resume_text}

Give the response in exactly these sections:

### Candidate Summary
Give a short summary of the candidate.

### Skills Found
List the technical and professional skills mentioned.

### Education
List the education information found.

### Projects
List the projects mentioned and briefly explain them.

### Experience
List internships, work experience, or other experience mentioned.

### Strengths
Mention strengths supported by the resume.

### Areas to Improve
Give practical suggestions for improving the resume.

### Missing Information
Mention useful information that is missing or unclear.

### Action Plan
Give practical next steps.

Rules:
- Do not invent information.
- If something is not mentioned, say "Not mentioned".
- Use simple language.
- Give practical suggestions.
"""
            with st.spinner("Reading your resume..."):
                try:
                    st.session_state.analysis_result = generate_ai(prompt)
                except Exception as e:
                    st.error(f"Gemini error: {e}")

        if st.session_state.analysis_result:
            st.divider()
            result_box("Analysis", st.session_state.analysis_result)

# ============================================================
# TAB 2 — JOB MATCH
# ============================================================

with match_tab:
    st.header("Resume & Job Match")
    st.markdown(
        '<div class="section-note">Compare your current resume with a specific job description and identify useful skill gaps.</div>',
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Paste the job description",
        placeholder=(
            "Example: We are looking for a Python developer with "
            "knowledge of SQL, Git, REST APIs..."
        ),
        height=230,
        key="job_description",
    )

    if st.button("Analyze Resume & Job Match", use_container_width=True, key="match_button"):
        if not require_resume():
            st.stop()
        if not job_description.strip():
            st.warning("Paste a job description first.")
            st.stop()

        prompt = f"""
You are ResumeLens AI, a professional career assistant.

Analyze the candidate's resume and compare it with the job description.

RESUME:
{st.session_state.resume_text}

JOB DESCRIPTION:
{job_description}

Give the result in these sections:

## 1. Resume Summary
Give a short summary of the candidate.

## 2. Matching Skills
List skills that appear in both the resume and job description.

## 3. Potential Skill Gaps
List important skills mentioned in the job description
that are not clearly shown in the resume.

## 4. Relevant Projects
Identify projects from the resume that are relevant to this job.

## 5. Relevant Experience
Identify internships or experience relevant to the job.

## 6. Resume Improvement Suggestions
Suggest specific things the candidate could improve
to make the resume more relevant to this role.

## 7. Skill Gap & Learning Plan

### Skills You Already Have
Skills from the job description that are clearly present in the resume.

### Skills You May Need to Develop
Important skills from the job description that are not clearly shown in the resume.

### Suggested Learning Order
Give a practical order for learning the missing skills.

For each important missing skill, briefly explain:
- Why it matters for this role
- What the candidate should learn first

Do not assume that a skill is missing if the resume simply describes it differently.
If uncertain, say "Not clearly mentioned".

## 8. Overall Match
Give an approximate resume-to-job match percentage.
Clearly explain that this is an AI-generated estimate,
not a hiring probability or guarantee.

Important:
- Only use information available in the resume and job description.
- Do not invent skills or experience.
- Keep the language simple.
- Give practical suggestions.
"""
        with st.spinner("Comparing your resume with the role..."):
            try:
                st.session_state.match_result = generate_ai(prompt)
            except Exception as e:
                st.error(f"Gemini error: {e}")

    if st.session_state.match_result:
        st.divider()
        result_box("Job Match Report", st.session_state.match_result)
        st.info(
            "The match percentage is an AI-generated estimate based on the provided resume and job description. "
            "It is not a hiring probability or guarantee."
        )

# ============================================================
# TAB 3 — RESUME TOOLS
# ============================================================

with tools_tab:
    st.header("Resume Tools")
    st.markdown(
        '<div class="section-note">Make individual parts of your resume clearer, stronger, and more professional without inventing achievements.</div>',
        unsafe_allow_html=True
    )

    bullet = st.text_area(
        "Resume bullet or experience description",
        placeholder="Example: Made a weather website using JavaScript.",
        height=140,
        key="resume_bullet",
    )

    if st.button("Improve Resume Bullet", use_container_width=True, key="bullet_button"):
        if not bullet.strip():
            st.warning("Enter a resume bullet first.")
            st.stop()

        bullet_prompt = f"""
You are a professional resume writing assistant.

Improve the following resume bullet for a student or fresher.

Original bullet:
{bullet}

Give the response in exactly these sections:

### Improved Version
Write one professional resume bullet.

### Why It Is Better
Give 2-3 simple points explaining the improvement.

### Information Missing
Mention useful details that could make the bullet stronger, such as:
- measurable results
- technologies used
- scale
- performance improvement
- user's contribution

Do NOT invent numbers, achievements, technologies,
or results that are not present in the original bullet.

Keep the improved version concise and truthful.
"""
        with st.spinner("Improving your bullet..."):
            try:
                st.session_state.bullet_result = generate_ai(bullet_prompt)
            except Exception as e:
                st.error(f"Gemini error: {e}")

    if st.session_state.bullet_result:
        st.divider()
        result_box("Improved Resume Content", st.session_state.bullet_result)

# ============================================================
# TAB 4 — PROJECT RECOMMENDATIONS
# ============================================================

with projects_tab:
    st.header("Project Recommendation Engine")
    st.markdown(
        '<div class="section-note">Find portfolio projects that connect your existing skills with the role you want.</div>',
        unsafe_allow_html=True
    )

    target_role = st.text_input(
        "Target role",
        placeholder="Example: AI/ML Intern",
        key="project_target_role",
    )

    if st.button("Suggest 3 Portfolio Projects", use_container_width=True, key="project_button"):
        if not require_resume():
            st.stop()
        if not target_role.strip():
            st.warning("Enter the role you are targeting first.")
            st.stop()

        prompt = f"""
You are an AI career and project recommendation assistant.

Analyze the student's resume and suggest practical projects
that can improve their portfolio for the target role.

TARGET ROLE:
{target_role}

JOB DESCRIPTION:
{job_description if 'job_description' in locals() and job_description.strip() else "Not provided"}

RESUME:
{st.session_state.resume_text}

Suggest exactly 3 project ideas.

For each project, give these sections:

### Project 1
- Project Title
- Problem It Solves
- Why It Is Relevant
- Skills/Technologies to Learn
- Main Features
- Difficulty Level
- Resume Bullet

### Project 2
- Project Title
- Problem It Solves
- Why It Is Relevant
- Skills/Technologies to Learn
- Main Features
- Difficulty Level
- Resume Bullet

### Project 3
- Project Title
- Problem It Solves
- Why It Is Relevant
- Skills/Technologies to Learn
- Main Features
- Difficulty Level
- Resume Bullet

Rules:
- Base suggestions on the resume, target role, and job description.
- Prefer projects that are practical and portfolio-worthy.
- Do not suggest projects that are unnecessarily complex for a student.
- Suggest projects that help develop missing or weak skills.
- Do not invent skills already present in the resume.
- Resume bullets must not contain fake numbers, achievements, or results.
- Keep the explanations simple and practical.
"""
        with st.spinner("Designing portfolio-ready ideas..."):
            try:
                st.session_state.project_result = generate_ai(prompt)
            except Exception as e:
                st.error(f"Gemini error: {e}")

    if st.session_state.project_result:
        st.divider()
        result_box("Recommended Projects", st.session_state.project_result)

# ============================================================
# TAB 5 — INTERVIEW
# ============================================================

with interview_tab:
    st.header("Interview Preparation")
    st.markdown(
        '<div class="section-note">Prepare from your actual resume instead of memorizing random interview questions.</div>',
        unsafe_allow_html=True
    )

    interview_role = st.text_input(
        "Target role for interview questions",
        placeholder="Example: Python Developer Intern",
        key="interview_role",
    )

    if st.button("Generate Interview Questions", use_container_width=True, key="interview_button"):
        if not require_resume():
            st.stop()
        if not interview_role.strip():
            st.warning("Enter your target role first.")
            st.stop()

        prompt = f"""
You are an experienced technical interviewer.

Create interview questions for a student/fresher based on
their resume and target role.

TARGET ROLE:
{interview_role}

RESUME:
{st.session_state.resume_text}

JOB DESCRIPTION:
{job_description if 'job_description' in locals() and job_description.strip() else "Not provided"}

Generate questions in exactly these sections:

### 1. Resume-Based Questions
Give 4 questions directly related to information in the resume.

### 2. Project Questions
Give 4 questions about the projects mentioned in the resume.

### 3. Technical Questions
Give 5 technical questions relevant to the target role
and technologies mentioned in the resume.

### 4. Problem-Solving Questions
Give 3 simple logical or practical questions relevant
to the target role.

### 5. HR Questions
Give 3 common fresher interview questions.

### Preparation Tips
Give 5 short tips for preparing for this interview.

Rules:
- Questions should be suitable for a student or fresher.
- Use the candidate's actual resume information.
- Do not invent projects, skills, experience, or achievements.
- Do not make questions unnecessarily difficult.
- Keep the questions clear and practical.
"""
        with st.spinner("Preparing your interview set..."):
            try:
                st.session_state.interview_result = generate_ai(prompt)
            except Exception as e:
                st.error(f"Gemini error: {e}")

    if st.session_state.interview_result:
        st.divider()
        result_box("Interview Question Set", st.session_state.interview_result)

    st.divider()
    st.subheader("Mock Interview")
    st.markdown(
        '<div class="section-note">Answer one question at a time and receive brief, constructive feedback.</div>',
        unsafe_allow_html=True
    )

    mock_role = st.text_input(
        "Role for mock interview",
        placeholder="Example: AI/ML Intern",
        key="mock_role",
    )

    start_col, reset_col = st.columns(2)

    with start_col:
        if st.button("Start Mock Interview", use_container_width=True, key="start_mock"):
            if not require_resume():
                st.stop()
            if not mock_role.strip():
                st.warning("Enter a role first.")
                st.stop()

            st.session_state.mock_history = []

            first_question_prompt = f"""
You are conducting a beginner-friendly technical interview.

Candidate target role:
{mock_role}

Candidate resume:
{st.session_state.resume_text}

Ask ONE interview question at a time.

Start with a simple introduction question.
Do not give the answer.
Do not ask multiple questions at once.
"""
            with st.spinner("Starting your interview..."):
                try:
                    first_response = generate_ai(first_question_prompt)
                    st.session_state.mock_history.append({
                        "role": "assistant",
                        "content": first_response,
                    })
                except Exception as e:
                    st.error(f"Gemini error: {e}")

    with reset_col:
        if st.button("Reset Interview", use_container_width=True, key="reset_mock"):
            st.session_state.mock_history = []
            st.rerun()

    if st.session_state.mock_history:
        st.markdown("### Live Interview")

        for message in st.session_state.mock_history:
            if message["role"] == "assistant":
                st.info("🎤 Interviewer\n\n" + message["content"])
            else:
                st.markdown(
                    f'<div class="result-card"><strong>👤 You</strong><br><br>{message["content"]}</div>',
                    unsafe_allow_html=True,
                )

        user_answer = st.text_area(
            "Your answer",
            placeholder="Type your answer here...",
            height=130,
            key="mock_answer",
        )

        if st.button("Submit Answer", use_container_width=True, key="submit_mock"):
            if not user_answer.strip():
                st.warning("Enter your answer first.")
                st.stop()

            previous_question = st.session_state.mock_history[-1]["content"]

            mock_prompt = f"""
You are conducting a beginner-friendly technical interview.

Target role:
{mock_role}

Candidate resume:
{st.session_state.resume_text}

Previous interviewer message:
{previous_question}

Candidate answer:
{user_answer}

Do these three things:

1. Give brief feedback on the answer.
2. Mention one thing the candidate did well.
3. Ask ONE relevant follow-up interview question.

Keep the feedback simple and constructive.
Do not invent information about the candidate.
Do not ask multiple questions at once.
"""
            with st.spinner("Reviewing your answer..."):
                try:
                    mock_response = generate_ai(mock_prompt)

                    st.session_state.mock_history.append({
                        "role": "user",
                        "content": user_answer,
                    })
                    st.session_state.mock_history.append({
                        "role": "assistant",
                        "content": mock_response,
                    })

                    st.rerun()

                except Exception as e:
                    st.error(f"Gemini error: {e}")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    <strong>ResumeLens AI</strong> · AI-powered resume & career workspace
    <br>
    Designed and built by <strong>Sai Ganesh</strong>
    <br>
    <span>Built with Python · Streamlit · Gemini</span>
</div>
""", unsafe_allow_html=True)
