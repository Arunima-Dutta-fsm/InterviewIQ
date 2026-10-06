import streamlit as st
from pypdf import PdfReader
from google import genai
from google.genai import types
import json
import re
import time


# ============================================================
# INTERVIEWIQ BRAND LOGO
# Embedded from the provided SVG so deployment needs no extra asset.
# ============================================================

INTERVIEWIQ_LOGO_SVG = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA3ODAgMTgwIiBmaWxsPSJub25lIj4KICA8ZGVmcz4KICAgIDwhLS0gVmlicmFudCBCbHVlLXRvLUN5YW4gR3JhZGllbnQgZm9yIHRoZSBJY29uIEJvcmRlciAmIElRIE1hcmsgLS0+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImlxR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjMUQ2OEZFIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiMwMEFFRUYiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgoKICAgIDwhLS0gU3VidGxlIEdsYXNzIEdsb3cgRmlsbCBpbnNpZGUgU3BlZWNoIEJ1YmJsZSAtLT4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iYnViYmxlRmlsbCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiNGRkZGRkYiIHN0b3Atb3BhY2l0eT0iMC4xMiIgLz4KICAgICAgPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjMDBBRUVGIiBzdG9wLW9wYWNpdHk9IjAuMDQiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogIDwvZGVmcz4KCiAgPCEtLSAxLiBJQ09OIE1BUksgLS0+CiAgPGcgaWQ9IlNwZWVjaEJ1YmJsZUljb24iPgogICAgPCEtLSBCdWJibGUgT3V0bGluZSAmIFRyYW5zbHVjZW50IEZpbGwgLS0+CiAgICA8cGF0aCBkPSJNIDU1IDI1IAogICAgICAgICAgICAgSCAxNDUgCiAgICAgICAgICAgICBBIDMwIDMwIDAgMCAxIDE3NSA1NSAKICAgICAgICAgICAgIFYgMTA1IAogICAgICAgICAgICAgQSAzMCAzMCAwIDAgMSAxNDUgMTM1IAogICAgICAgICAgICAgSCA4MiAKICAgICAgICAgICAgIEwgNTIgMTYyIAogICAgICAgICAgICAgTCA2MCAxMzUgCiAgICAgICAgICAgICBIIDU1IAogICAgICAgICAgICAgQSAzMCAzMCAwIDAgMSAyNSAxMDUgCiAgICAgICAgICAgICBWIDU1IAogICAgICAgICAgICAgQSAzMCAzMCAwIDAgMSA1NSAyNSBaIiAKICAgICAgICAgIGZpbGw9InVybCgjYnViYmxlRmlsbCkiIAogICAgICAgICAgc3Ryb2tlPSJ1cmwoI2lxR3JhZGllbnQpIiAKICAgICAgICAgIHN0cm9rZS13aWR0aD0iMTAiIAogICAgICAgICAgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiAKICAgICAgICAgIHN0cm9rZS1saW5lam9pbj0icm91bmQiIC8+CgogICAgPCEtLSBOZXVyYWwgTmV0d29yayBOb2RlcyAmIExpbmtzIGluc2lkZSBCdWJibGUgLS0+CiAgICA8ZyBpZD0iU3luYXBzZUdyYXBoIj4KICAgICAgPCEtLSBVcHBlciBkYXNoZWQgbGluayAtLT4KICAgICAgPGxpbmUgeDE9IjY4IiB5MT0iNjIiIHgyPSIxMTQiIHkyPSI1OCIgc3Ryb2tlPSIjMDBBRUVGIiBzdHJva2Utd2lkdGg9IjUiIHN0cm9rZS1kYXNoYXJyYXk9IjYgNiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiAvPgogICAgICA8IS0tIFJpZ2h0IHZlcnRpY2FsIGxpbmsgLS0+CiAgICAgIDxsaW5lIHgxPSIxMTQiIHkxPSI1OCIgeDI9IjEyNCIgeTI9IjkyIiBzdHJva2U9IiMwMEFFRUYiIHN0cm9rZS13aWR0aD0iNSIgc3Ryb2tlLWRhc2hhcnJheT0iNiA2IiBzdHJva2UtbGluZWNhcD0icm91bmQiIC8+CiAgICAgIDwhLS0gU29saWQgYmFzZWxpbmUgJiB1cHdhcmQgdHJhamVjdG9yeSAtLT4KICAgICAgPHBvbHlsaW5lIHBvaW50cz0iNjgsNjIgNzYsOTYgMTI0LDkyIDE0NCw2NiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ1cmwoI2lxR3JhZGllbnQpIiBzdHJva2Utd2lkdGg9IjYuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiAvPgogICAgICAKICAgICAgPCEtLSBOb2RlcyAvIFN5bmFwc2VzIC0tPgogICAgICA8Y2lyY2xlIGN4PSI2OCIgY3k9IjYyIiByPSIxMCIgZmlsbD0iIzI1NjNFQiIgLz4KICAgICAgPGNpcmNsZSBjeD0iMTE0IiBjeT0iNTgiIHI9IjkiIGZpbGw9IiMwMEQyRkYiIC8+CiAgICAgIDxjaXJjbGUgY3g9Ijc2IiBjeT0iOTYiIHI9IjkuNSIgZmlsbD0iIzFENjhGRSIgLz4KICAgICAgPGNpcmNsZSBjeD0iMTI0IiBjeT0iOTIiIHI9IjguNSIgZmlsbD0iIzAwQzBGMyIgLz4KICAgICAgPGNpcmNsZSBjeD0iMTQ0IiBjeT0iNjYiIHI9IjciIGZpbGw9IiMwMEQyRkYiIC8+CiAgICA8L2c+CiAgPC9nPgoKICA8IS0tIDIuIE1BSU4gV09SRE1BUksgLS0+CiAgPGcgaWQ9IkxvZ29UZXh0Ij4KICAgIDwhLS0gIkludGVydmlldyIgaW4gUHVyZSBXaGl0ZSAtLT4KICAgIDx0ZXh0IHg9IjIxNSIgeT0iOTYiIAogICAgICAgICAgZm9udC1mYW1pbHk9IidQbHVzIEpha2FydGEgU2FucycsICdJbnRlcicsIHN5c3RlbS11aSwgc2Fucy1zZXJpZiIgCiAgICAgICAgICBmb250LXNpemU9Ijc4IiAKICAgICAgICAgIGZvbnQtd2VpZ2h0PSI4MDAiIAogICAgICAgICAgZmlsbD0iI0ZGRkZGRiIgCiAgICAgICAgICBsZXR0ZXItc3BhY2luZz0iLTEuNSI+SW50ZXJ2aWV3PC90ZXh0PgoKICAgIDwhLS0gIklRIiBpbiBHcmFkaWVudCAtLT4KICAgIDx0ZXh0IHg9IjYxOCIgeT0iOTYiIAogICAgICAgICAgZm9udC1mYW1pbHk9IidQbHVzIEpha2FydGEgU2FucycsICdJbnRlcicsIHN5c3RlbS11aSwgc2Fucy1zZXJpZiIgCiAgICAgICAgICBmb250LXNpemU9Ijc4IiAKICAgICAgICAgIGZvbnQtd2VpZ2h0PSI4MDAiIAogICAgICAgICAgZmlsbD0idXJsKCNpcUdyYWRpZW50KSIgCiAgICAgICAgICBsZXR0ZXItc3BhY2luZz0iLTAuNSI+SVE8L3RleHQ+CiAgPC9nPgoKICA8IS0tIDMuIFNVQlRJVExFIC8gVEFHTElORSAtLT4KICA8dGV4dCB4PSIyMTgiIHk9IjEzOCIgCiAgICAgICAgZm9udC1mYW1pbHk9IidJbnRlcicsIHN5c3RlbS11aSwgc2Fucy1zZXJpZiIgCiAgICAgICAgZm9udC1zaXplPSIxOSIgCiAgICAgICAgZm9udC13ZWlnaHQ9IjcwMCIgCiAgICAgICAgZmlsbD0iIzk0QTNCOCIgCiAgICAgICAgbGV0dGVyLXNwYWNpbmc9IjciPkFEQVBUSVZFIEFJIElOVEVSVklFV0VSPC90ZXh0Pgo8L3N2Zz4K"



# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="InterviewIQ",
    page_icon="🎯",
    layout="wide"
)



# ============================================================
# INTERVIEWIQ VISUAL THEME
# ============================================================

st.markdown(
    """
    <style>
    /* ---------- App background ---------- */
    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(99, 102, 241, 0.13), transparent 28%),
            radial-gradient(circle at 92% 8%, rgba(14, 165, 233, 0.10), transparent 25%),
            linear-gradient(145deg, #080b14 0%, #0d111c 48%, #0a0f19 100%);
        color: #eef2ff;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    [data-testid="stHeader"] {
        background: rgba(8, 11, 20, 0.72);
        backdrop-filter: blur(12px);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Typography ---------- */
    h1 {
        font-size: 2.45rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em;
        background: linear-gradient(90deg, #ffffff 0%, #c7d2fe 45%, #67e8f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.15rem !important;
    }

    h2 {
        color: #f8fafc !important;
        font-weight: 750 !important;
        letter-spacing: -0.02em;
        margin-top: 1.3rem !important;
    }

    h3 {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }

    p, label, .stCaption {
        color: #cbd5e1;
    }

    /* ---------- Horizontal rules ---------- */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(129, 140, 248, 0.45),
            rgba(34, 211, 238, 0.28),
            transparent
        ) !important;
        margin: 1.5rem 0 !important;
    }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploader"] {
        background: rgba(17, 24, 39, 0.72);
        border: 1px solid rgba(129, 140, 248, 0.22);
        border-radius: 14px;
        padding: 0.35rem;
        transition: all 0.2s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(103, 232, 249, 0.45);
        box-shadow: 0 0 28px rgba(59, 130, 246, 0.08);
    }

    /* ---------- Inputs ---------- */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background: rgba(17, 24, 39, 0.92) !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 11px !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1, 0 0 18px rgba(99, 102, 241, 0.14) !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 10px !important;
        border: 1px solid rgba(129, 140, 248, 0.32) !important;
        background: linear-gradient(135deg, #4f46e5, #2563eb) !important;
        color: white !important;
        font-weight: 700 !important;
        min-height: 2.65rem;
        box-shadow: 0 8px 22px rgba(37, 99, 235, 0.18);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 28px rgba(59, 130, 246, 0.27);
        border-color: rgba(165, 180, 252, 0.65) !important;
    }

    /* ---------- Alerts / info cards ---------- */
    [data-testid="stAlert"] {
        border-radius: 11px !important;
        border: 1px solid rgba(148, 163, 184, 0.18) !important;
        background: rgba(15, 23, 42, 0.72) !important;
    }

    /* ---------- Expanders ---------- */
    [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.58);
        border: 1px solid rgba(100, 116, 139, 0.26);
        border-radius: 11px;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary:hover {
        background: rgba(99, 102, 241, 0.08);
    }

    /* ---------- Metric cards ---------- */
    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.78),
            rgba(15, 23, 42, 0.76)
        );
        border: 1px solid rgba(129, 140, 248, 0.20);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        min-height: 105px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.16);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 650 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 800 !important;
    }

    /* ---------- Code/text preview ---------- */
    [data-testid="stText"] {
        background: #0b1220;
        border-radius: 10px;
    }

    /* ---------- Success / warning / error ---------- */
    [data-testid="stAlert"][kind="success"] {
        border-color: rgba(34, 197, 94, 0.28) !important;
    }

    /* ---------- Current interview question ---------- */
    .stInfo {
        border-radius: 13px !important;
    }

    /* ---------- Progress ---------- */
    [data-testid="stProgressBar"] {
        border-radius: 999px;
    }

    /* ---------- Spacing ---------- */
    .block-container {
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* ---------- Mobile ---------- */
    @media (max-width: 768px) {
        [data-testid="stMainBlockContainer"] {
            padding-top: 1rem;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 1.9rem !important;
        }

        h2 {
            font-size: 1.35rem !important;
        }

        [data-testid="stMetric"] {
            min-height: 90px;
            padding: 0.8rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# GEMINI SETUP
# ============================================================

try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    client = None

MODEL_NAME = "gemini-3.8-flash"

# Primary + fallback model strategy
MODEL_STRATEGY = [
    ("gemini-3.8-flash", 3),       # Primary: 3 attempts
    ("gemini-3.7-flash", 2),
    ("gemini-3.6-flash", 2),
    ("gemini-3.5-flash", 2),
    ("gemini-3.5-flash-lite", 2),
]

TOTAL_QUESTIONS = 12

# Performance settings
# Low thinking is intentional here: interview scoring/question generation
# benefits from fast structured output more than long reasoning.
THINKING_LEVEL = "low"
MAX_OUTPUT_TOKENS = 1500
RECENT_HISTORY_COUNT = 3

TEMPORARY_ERRORS = [
    "503",
    "UNAVAILABLE",
    "429",
    "RESOURCE_EXHAUSTED",
    "500",
    "502",
    "504",
    "INTERNAL",
    "DEADLINE_EXCEEDED",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def extract_pdf_text(uploaded_file):
    """Extract text from an uploaded PDF."""
    try:
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def clean_json_response(text):
    """Clean Gemini response so it can be parsed as JSON."""
    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Find JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return text.strip()


def call_gemini(prompt):
    """Fast Gemini call with the required fallback strategy."""

    if client is None:
        raise Exception(
            "Gemini client could not be initialized. "
            "Please check GEMINI_API_KEY in .streamlit/secrets.toml."
        )

    last_error = None
    call_started = time.perf_counter()

    for model_name, max_attempts in MODEL_STRATEGY:
        for attempt in range(1, max_attempts + 1):
            try:
                start_time = time.perf_counter()

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        thinking_config=types.ThinkingConfig(
                            thinking_level=THINKING_LEVEL
                        ),
                        max_output_tokens=MAX_OUTPUT_TOKENS
                    )
                )

                elapsed = time.perf_counter() - start_time

                if response and response.text:
                    request_seconds = round(elapsed, 1)
                    total_elapsed = round(time.perf_counter() - call_started, 1)
                    st.session_state.last_model_used = model_name
                    st.session_state.last_gemini_seconds = total_elapsed
                    st.session_state.gemini_call_log.append({
                        "model": model_name,
                        "seconds": total_elapsed,
                        "request_seconds": request_seconds,
                    })
                    return response.text

                raise Exception("Gemini returned an empty response.")

            except Exception as e:
                last_error = e
                error_message = str(e)

                is_temporary_error = any(
                    error_code in error_message
                    for error_code in TEMPORARY_ERRORS
                )

                # Permanent errors surface immediately.
                if not is_temporary_error:
                    raise e

                # Fast retry backoff: 1s, then 2s.
                if attempt < max_attempts:
                    time.sleep(2 ** (attempt - 1))

    raise Exception(
        "Gemini service is temporarily unavailable across all configured "
        "fallback models. Please try again later. "
        f"Last error: {last_error}"
    )


# ============================================================
# INITIAL CANDIDATE + JD ANALYSIS + FIRST QUESTION
# ONE GEMINI CALL INSTEAD OF TWO
# ============================================================

def analyze_candidate_and_create_first_question(
    resume_text,
    jd_text,
    role
):
    """
    Analyze the candidate and JD and create Question 1
    in the same Gemini call to reduce startup latency.
    """

    # Keep unusually large documents from inflating the request.
    resume_for_ai = resume_text[:15000]
    jd_for_ai = jd_text[:15000]

    prompt = f"""
You are an expert corporate interviewer, recruitment consultant,
and assessment designer.

We are building an adaptive mock interview for the target role below.

TARGET ROLE:
{role}

CANDIDATE RESUME:
{resume_for_ai}

JOB DESCRIPTION:
{jd_for_ai}

Analyze the candidate and job description carefully.

Identify:
1. Candidate education
2. Candidate work experience
3. Technical skills
4. Business/functional skills
5. Projects
6. Certifications
7. Key achievements
8. Relevant strengths
9. Potential gaps
10. Important competencies required by the JD

Then create the FIRST interview question.

The first question should normally be a professional warm-up,
but it must still be personalized using the candidate's actual
background and aligned with the target role.

Return ONLY valid JSON in this exact structure:

{{
    "profile": {{
        "candidate_summary": "...",
        "education": ["..."],
        "experience": ["..."],
        "technical_skills": ["..."],
        "functional_skills": ["..."],
        "projects": ["..."],
        "certifications": ["..."],
        "strengths": ["..."],
        "gaps": ["..."],
        "jd_competencies": ["..."]
    }},
    "first_question": {{
        "question": "...",
        "competency": "...",
        "difficulty": "Warm-up",
        "reason": "Brief explanation of why this question was selected"
    }}
}}
"""

    result = call_gemini(prompt)
    result = clean_json_response(result)

    return json.loads(result)


# ============================================================
# EVALUATE ANSWER + GENERATE NEXT QUESTION
# ONE GEMINI CALL PER ANSWER
# ============================================================

def evaluate_answer_and_create_next_question(
    profile,
    role,
    question,
    answer,
    competency,
    difficulty,
    previous_questions,
    previous_answers,
    question_number
):
    """
    In ONE Gemini call:
    1. Evaluate the current answer
    2. Decide the appropriate next difficulty
    3. Generate the next personalized question

    This replaces the old two-call flow:
        evaluate_answer() + generate_question()
    """

    # Only the most recent exchanges are needed for adaptive continuity.
    # Sending the full 12-question history makes later calls increasingly slow.
    history = ""
    recent_count = min(RECENT_HISTORY_COUNT, len(previous_questions))
    start_index = len(previous_questions) - recent_count

    for i in range(start_index, len(previous_questions)):
        history += f"""
Question {i + 1}:
{previous_questions[i]}

Candidate Answer:
{previous_answers[i][:4000]}
"""

    is_last_question = question_number >= TOTAL_QUESTIONS

    next_question_instruction = """
Generate the next interview question.

The next question must:
- Be different from previous questions.
- Be personalized using the candidate profile.
- Align with the target role and JD competencies.
- Build naturally on the candidate's previous response.
- Increase difficulty when the answer is strong.
- Maintain or slightly reduce difficulty when the answer is average.
- Ask a clarifying/easier question if the answer is weak.
- Feel like a realistic corporate interview question.
- Avoid generic filler questions.
- Never reveal the expected answer.
""" if not is_last_question else """
This is the final interview question.

Do NOT generate another question.
Set "next_question" to null.
"""

    prompt = f"""
You are an expert corporate interviewer conducting an adaptive
interview for the following target role:

TARGET ROLE:
{role}

CANDIDATE PROFILE:
{json.dumps(profile, separators=(",", ":"))}

CURRENT QUESTION:
{question}

COMPETENCY:
{competency}

CURRENT DIFFICULTY:
{difficulty}

CANDIDATE ANSWER:
{answer}

PREVIOUS INTERVIEW HISTORY:
{history if history else "This is the first answered question."}

QUESTION NUMBER:
{question_number} of {TOTAL_QUESTIONS}

Evaluate the candidate using this fixed scoring rubric:

Relevance = 25%
Accuracy = 30%
Depth = 20%
Communication = 15%
Role/JD Alignment = 10%

Give each component score between 0 and 10.

Calculate the weighted overall score out of 10.

Also provide:
- What the candidate did well
- What could be improved
- One concise interview tip

Then determine the next appropriate difficulty.

Difficulty options:
- Warm-up
- Moderate
- Moderate-Advanced
- Advanced
- Expert
- Cross-question

Adaptive rule:
- Overall score >= 8: generally increase difficulty.
- Overall score 6 to 7.9: maintain or moderately increase difficulty.
- Overall score < 6: maintain or reduce difficulty and test the weak area.
- Do not make the interview artificially easier or harder without reason.

{next_question_instruction}

Return ONLY valid JSON in this exact structure:

{{
    "evaluation": {{
        "relevance": 0,
        "accuracy": 0,
        "depth": 0,
        "communication": 0,
        "jd_alignment": 0,
        "overall_score": 0,
        "strength": "...",
        "improvement": "...",
        "tip": "..."
    }},
    "next_question": {{
        "question": "...",
        "competency": "...",
        "difficulty": "...",
        "reason": "Brief explanation of why this question was selected"
    }}
}}

For the final question, return:

"next_question": null
"""

    result = call_gemini(prompt)
    result = clean_json_response(result)

    return json.loads(result)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "interview_started": False,
    "profile": None,
    "questions": [],
    "answers": [],
    "evaluations": [],
    "current_question": None,
    "current_competency": None,
    "current_difficulty": None,
    "interview_complete": False,
    "last_model_used": None,
    "last_gemini_seconds": None,
    "gemini_call_log": [],
    "app_stage": "setup",
    "target_role": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div style="
        width:100%;
        display:flex;
        justify-content:flex-start;
        align-items:center;
        margin:0 0 0.75rem 0;
    ">
        <img
            src="data:image/svg+xml;base64,{INTERVIEWIQ_LOGO_SVG}"
            alt="InterviewIQ — Adaptive AI Interviewer"
            style="
                width:min(520px, 82vw);
                height:auto;
                display:block;
            "
        />
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        margin:0 0 1.25rem 0;
        color:#94a3b8;
        font-size:0.96rem;
        max-width:850px;
        line-height:1.65;
    ">
        A personalized AI mock-interview platform that analyzes your
        <span style="color:#c7d2fe;font-weight:650;">Resume</span> and
        <span style="color:#67e8f9;font-weight:650;">Job Description</span>
        to conduct an adaptive, role-specific interview.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE 1 — SETUP
# ============================================================

if st.session_state.app_stage == "setup":

    st.divider()

    st.header("📄 Step 1: Upload Your Resume")

    resume_file = st.file_uploader(
        "Upload your Resume",
        type=["pdf"],
        key="resume"
    )

    resume_text = ""

    if resume_file:
        resume_text = extract_pdf_text(resume_file)
        st.success(f"Resume uploaded successfully: {resume_file.name}")
        with st.expander("🔍 Preview Extracted Resume Text"):
            st.text(resume_text)

    st.header("📋 Step 2: Upload the Job Description")

    jd_file = st.file_uploader(
        "Upload the Job Description",
        type=["pdf"],
        key="jd"
    )

    jd_text = ""

    if jd_file:
        jd_text = extract_pdf_text(jd_file)
        st.success(f"Job Description uploaded successfully: {jd_file.name}")
        with st.expander("🔍 Preview Extracted Job Description"):
            st.text(jd_text)

    st.header("🎯 Step 3: Enter the Target Role")

    role = st.text_input(
        "What role are you interviewing for?",
        placeholder="Example: Digital Sales Executive",
        key="target_role"
    )

    st.header("🚀 Step 4: Start Your Interview")

    ready = resume_file and jd_file and role.strip()

    if ready:
        if st.button("🚀 Start Interview", type="primary", use_container_width=True):
            with st.spinner("Analyzing your Resume and Job Description..."):
                try:
                    initial_result = analyze_candidate_and_create_first_question(
                        resume_text, jd_text, role
                    )
                    profile = initial_result["profile"]
                    first_question = initial_result["first_question"]

                    st.session_state.profile = profile
                    # target_role is already bound to the text_input widget.
                    # Do not modify st.session_state.target_role after the
                    # widget has been instantiated, or Streamlit raises a
                    # StreamlitAPIException.
                    st.session_state.current_question = first_question["question"]
                    st.session_state.current_competency = first_question["competency"]
                    st.session_state.current_difficulty = first_question["difficulty"]
                    st.session_state.questions = []
                    st.session_state.answers = []
                    st.session_state.evaluations = []
                    # call_gemini logs the startup call; do not erase it here.
                    st.session_state.interview_started = True
                    st.session_state.interview_complete = False
                    st.session_state.app_stage = "interview"
                    st.rerun()
                except Exception as e:
                    st.error(f"Something went wrong while starting the interview: {e}")
    else:
        st.info(
            "Please upload your Resume, upload the Job Description, "
            "and enter the target role."
        )


# ============================================================
# INTERVIEW ENGINE
# ============================================================


if st.session_state.app_stage == "interview":

    st.divider()

    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            padding:1rem 1.2rem;
            border-radius:15px;
            background:linear-gradient(135deg, rgba(30,41,59,0.85), rgba(15,23,42,0.72));
            border:1px solid rgba(99,102,241,0.22);
            margin-bottom:1rem;
        ">
            <span style="font-size:1.7rem;">🎤</span>
            <div>
                <div style="font-size:1.35rem;font-weight:800;color:#f8fafc;">
                    Your AI Interview
                </div>
                <div style="font-size:0.85rem;color:#94a3b8;">
                    Answer naturally — InterviewIQ adapts the next question based on your response.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.last_gemini_seconds is not None:
        st.caption(
            f"⚡ Last AI response: {st.session_state.last_gemini_seconds:.1f}s "
            f"• Engine: {st.session_state.last_model_used}"
        )

    submitted_count = len(st.session_state.questions)

    # --------------------------------------------------------
    # SHOW PREVIOUS QUESTIONS + ANSWERS
    # --------------------------------------------------------

    if submitted_count > 0:

        st.subheader("📚 Interview History")

        for i in range(submitted_count):

            evaluation = st.session_state.evaluations[i]

            with st.container():

                st.markdown(
                    f"### Question {i + 1}"
                )

                st.info(
                    st.session_state.questions[i]
                )

                st.markdown(
                    "**Your Answer:**"
                )

                st.write(
                    st.session_state.answers[i]
                )

                score = evaluation.get("overall_score", 0)

                st.markdown(
                    f"**Score:** {score}/10"
                )

                with st.expander("View AI Evaluation"):

                    st.write(
                        f"**Strength:** "
                        f"{evaluation.get('strength', '')}"
                    )

                    st.write(
                        f"**Improvement:** "
                        f"{evaluation.get('improvement', '')}"
                    )

                    st.write(
                        f"**Interview Tip:** "
                        f"{evaluation.get('tip', '')}"
                    )

                    st.write(
                        f"**Relevance:** "
                        f"{evaluation.get('relevance', 0)}/10"
                    )

                    st.write(
                        f"**Accuracy:** "
                        f"{evaluation.get('accuracy', 0)}/10"
                    )

                    st.write(
                        f"**Depth:** "
                        f"{evaluation.get('depth', 0)}/10"
                    )

                    st.write(
                        f"**Communication:** "
                        f"{evaluation.get('communication', 0)}/10"
                    )

                    st.write(
                        f"**JD Alignment:** "
                        f"{evaluation.get('jd_alignment', 0)}/10"
                    )

                st.divider()

    # --------------------------------------------------------
    # CURRENT QUESTION
    # --------------------------------------------------------

    question_number = submitted_count + 1

    st.caption(
        f"Question {question_number} of {TOTAL_QUESTIONS}"
    )

    progress_fraction = min(submitted_count / TOTAL_QUESTIONS, 1.0)

    if question_number <= 4:
        progress_color = "#ef4444"
        progress_label = "Warm-up phase"
    elif question_number <= 8:
        progress_color = "#eab308"
        progress_label = "Core assessment phase"
    else:
        progress_color = "#22c55e"
        progress_label = "Advanced assessment phase"

    st.markdown(
        f"""
        <div style="margin:8px 0 18px 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-size:0.85rem;font-weight:600;">Progress</span>
                <span style="font-size:0.8rem;opacity:0.8;">{progress_label}</span>
            </div>
            <div style="width:100%;height:10px;background:#2b2f38;border-radius:999px;overflow:hidden;">
                <div style="width:{progress_fraction * 100:.1f}%;height:100%;background:{progress_color};border-radius:999px;transition:width 0.3s ease;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        st.session_state.current_question
    )

    st.write(
        f"**Competency:** "
        f"{st.session_state.current_competency}"
    )

    st.write(
        f"**Difficulty:** "
        f"{st.session_state.current_difficulty}"
    )

    answer = st.text_area(
        "Your Answer",
        placeholder="Type your answer here...",
        height=180,
        key=f"answer_{question_number}"
    )

    if st.button(
        "Submit Answer →",
        type="primary",
        use_container_width=True,
        key=f"submit_{question_number}"
    ):

        if not answer.strip():

            st.warning(
                "Please enter an answer before submitting."
            )

        else:

            with st.spinner(
                "AI is evaluating your answer and preparing the next question..."
            ):

                try:

                    # ONE Gemini call:
                    # evaluation + adaptive difficulty + next question.
                    result = evaluate_answer_and_create_next_question(
                        profile=st.session_state.profile,
                        role=st.session_state.target_role,
                        question=st.session_state.current_question,
                        answer=answer,
                        competency=st.session_state.current_competency,
                        difficulty=st.session_state.current_difficulty,
                        previous_questions=st.session_state.questions,
                        previous_answers=st.session_state.answers,
                        question_number=question_number
                    )

                    evaluation = result["evaluation"]

                    # Store current question, answer and evaluation.
                    st.session_state.questions.append(
                        st.session_state.current_question
                    )

                    st.session_state.answers.append(
                        answer
                    )

                    st.session_state.evaluations.append(
                        evaluation
                    )

                    # ------------------------------------------------
                    # INTERVIEW COMPLETE AFTER 12 QUESTIONS
                    # ------------------------------------------------

                    if question_number >= TOTAL_QUESTIONS:

                        st.session_state.interview_complete = True
                        st.session_state.app_stage = "report"

                        st.rerun()

                    # ------------------------------------------------
                    # MOVE TO NEXT QUESTION
                    # ------------------------------------------------

                    else:

                        next_question = result.get("next_question")

                        if not next_question:
                            raise Exception(
                                "The AI did not return the next interview question."
                            )

                        st.session_state.current_question = (
                            next_question["question"]
                        )

                        st.session_state.current_competency = (
                            next_question["competency"]
                        )

                        st.session_state.current_difficulty = (
                            next_question["difficulty"]
                        )

                        st.rerun()

                except Exception as e:

                    st.error(
                        f"Error processing your answer: {e}"
                    )


# ============================================================
# FINAL REPORT
# ============================================================

if st.session_state.app_stage == "report" and st.session_state.interview_complete:

    st.divider()

    st.markdown(
        """
        <div style="
            padding:1.15rem 1.35rem;
            border-radius:16px;
            background:linear-gradient(135deg, rgba(79,70,229,0.16), rgba(14,165,233,0.10));
            border:1px solid rgba(129,140,248,0.25);
            margin-bottom:1.2rem;
        ">
            <div style="font-size:1.75rem;font-weight:800;color:#f8fafc;">
                📊 Interview Performance Report
            </div>
            <div style="color:#94a3b8;margin-top:0.25rem;">
                Your performance across all 12 adaptive interview questions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    evaluations = st.session_state.evaluations

    if evaluations:

        # Calculate average scores.
        avg_score = sum(
            e.get("overall_score", 0)
            for e in evaluations
        ) / len(evaluations)

        avg_relevance = sum(
            e.get("relevance", 0)
            for e in evaluations
        ) / len(evaluations)

        avg_accuracy = sum(
            e.get("accuracy", 0)
            for e in evaluations
        ) / len(evaluations)

        avg_depth = sum(
            e.get("depth", 0)
            for e in evaluations
        ) / len(evaluations)

        avg_communication = sum(
            e.get("communication", 0)
            for e in evaluations
        ) / len(evaluations)

        avg_alignment = sum(
            e.get("jd_alignment", 0)
            for e in evaluations
        ) / len(evaluations)

        # --------------------------------------------------------
        # SCORE
        # --------------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Overall Score",
                f"{avg_score:.1f}/10"
            )

        with col2:
            st.metric(
                "Questions",
                len(evaluations)
            )

        with col3:

            if avg_score >= 8:
                level = "Excellent"

            elif avg_score >= 6:
                level = "Good"

            elif avg_score >= 4:
                level = "Needs Improvement"

            else:
                level = "Needs Significant Improvement"

            st.metric(
                "Interview Readiness",
                level
            )

        # --------------------------------------------------------
        # COMPETENCY SCORES
        # --------------------------------------------------------

        st.subheader("📈 Competency Breakdown")

        competency_data = {
            "Relevance": avg_relevance,
            "Accuracy": avg_accuracy,
            "Depth": avg_depth,
            "Communication": avg_communication,
            "JD Alignment": avg_alignment
        }

        for competency_name, score in competency_data.items():

            st.write(
                f"**{competency_name}: {score:.1f}/10**"
            )

            st.progress(
                min(score / 10, 1.0)
            )

        # --------------------------------------------------------
        # QUESTION-WISE FEEDBACK
        # --------------------------------------------------------

        st.subheader("📝 Question-wise Feedback")

        for i, evaluation in enumerate(evaluations):

            with st.expander(
                f"Question {i + 1} — "
                f"Score: {evaluation.get('overall_score', 0)}/10"
            ):

                st.write(
                    f"**Question:** "
                    f"{st.session_state.questions[i]}"
                )

                st.write(
                    f"**Your Answer:** "
                    f"{st.session_state.answers[i]}"
                )

                st.write(
                    f"**Strength:** "
                    f"{evaluation.get('strength', '')}"
                )

                st.write(
                    f"**Improvement:** "
                    f"{evaluation.get('improvement', '')}"
                )

                st.write(
                    f"**Interview Tip:** "
                    f"{evaluation.get('tip', '')}"
                )

        # --------------------------------------------------------
        # FINAL RECOMMENDATION
        # --------------------------------------------------------

        st.subheader("🎯 Final Recommendation")

        competency_scores = {
            "Relevance": avg_relevance,
            "Accuracy": avg_accuracy,
            "Depth": avg_depth,
            "Communication": avg_communication,
            "JD Alignment": avg_alignment,
        }

        weakest_name = min(competency_scores, key=competency_scores.get)
        strongest_name = max(competency_scores, key=competency_scores.get)
        weakest_score = competency_scores[weakest_name]
        strongest_score = competency_scores[strongest_name]

        if avg_score >= 8:
            recommendation = (
                f"You demonstrated strong overall readiness for the target role, "
                f"with an average score of {avg_score:.1f}/10. Your strongest area "
                f"was {strongest_name} ({strongest_score:.1f}/10), indicating that "
                f"you can communicate relevant and role-aligned responses under interview pressure.\n\n"
                f"To move from strong to excellent, focus particularly on {weakest_name} "
                f"({weakest_score:.1f}/10). Continue practising scenario-based questions, "
                "quantifying your impact with specific examples, and maintaining consistent "
                "quality across technical, behavioural and role-specific questions."
            )
            st.success(recommendation)

        elif avg_score >= 6:
            recommendation = (
                f"You show a reasonable level of interview readiness with an average score "
                f"of {avg_score:.1f}/10. Your strongest dimension was {strongest_name} "
                f"({strongest_score:.1f}/10), which gives you a good foundation for the role.\n\n"
                f"Your main development priority should be {weakest_name} ({weakest_score:.1f}/10). "
                "Before the actual interview, practise structuring answers with a clear "
                "Situation–Task–Action–Result flow, connect every answer explicitly to the "
                "job requirements, and support claims with concrete examples, metrics or outcomes. "
                "A few targeted practice rounds in the weakest area should improve consistency "
                "and overall confidence."
            )
            st.warning(recommendation)

        else:
            recommendation = (
                f"Your current average score of {avg_score:.1f}/10 suggests that additional "
                "preparation would be valuable before the actual interview. The strongest "
                f"dimension was {strongest_name} ({strongest_score:.1f}/10), but the overall "
                "performance indicates that the core competencies are not yet consistent.\n\n"
                f"Start by strengthening {weakest_name} ({weakest_score:.1f}/10), then revise "
                "the fundamentals of the target role and prepare 5–6 strong examples from your "
                "education, projects and work experience. Practise concise, structured answers "
                "and repeat the interview until your responses become more accurate, specific and "
                "closely aligned with the JD."
            )
            st.error(recommendation)

        st.markdown("**Recommended next steps:**")
        st.markdown(
            f"1. **Strengthen {weakest_name}:** practise targeted questions in this area.\n"
            "2. **Use evidence:** support answers with measurable outcomes, examples and business impact.\n"
            "3. **Stay structured:** use STAR for behavioural/situational questions and a clear point–reason–example structure for analytical questions.\n"
            "4. **Reattempt the interview:** use the same Resume/JD after preparation and compare your scores."
        )

        # --------------------------------------------------------
        # AI RESPONSE PERFORMANCE
        # --------------------------------------------------------

        st.subheader("⚡ AI Response Performance")

        call_log = st.session_state.gemini_call_log

        if call_log:
            times = [entry["seconds"] for entry in call_log]
            avg_time = sum(times) / len(times)
            fastest = min(times)
            slowest = max(times)
            total_time = sum(times)

            t1, t2, t3, t4 = st.columns(4)
            with t1:
                st.metric("AI Calls", len(call_log))
            with t2:
                st.metric("Average Response", f"{avg_time:.1f}s")
            with t3:
                st.metric("Fastest", f"{fastest:.1f}s")
            with t4:
                st.metric("Slowest", f"{slowest:.1f}s")

            st.caption(
                f"Total Gemini processing time across the interview: {total_time:.1f}s. "
                "These are wall-clock times from entering the Gemini call until a successful response, including any retry/fallback wait. Browser rendering and file upload time are excluded."
            )

            with st.expander("View AI Call Timing Details"):
                for idx, entry in enumerate(call_log, start=1):
                    call_type = "Startup / Question 1" if idx == 1 else f"Evaluation + Question {idx}"
                    request_part = entry.get("request_seconds", entry["seconds"])
                    st.write(
                        f"**Call {idx} — {call_type}:** {entry['seconds']:.1f}s total "
                        f"({request_part:.1f}s model request, {entry['model']})"
                    )

        if st.session_state.last_model_used:
            st.caption(
                f"Last successful AI engine: {st.session_state.last_model_used} "
                "(automatic fallback enabled)"
            )

        # --------------------------------------------------------
        # RESTART
        # --------------------------------------------------------

        if st.button(
            "🔄 Start New Interview",
            use_container_width=True
        ):

            keys_to_reset = [
                "interview_started",
                "profile",
                "questions",
                "answers",
                "evaluations",
                "current_question",
                "current_competency",
                "current_difficulty",
                "interview_complete",
                "last_model_used",
                "last_gemini_seconds",
                "gemini_call_log",
                "resume",
                "jd",
                "target_role",
            ]

            for key in keys_to_reset:
                if key in st.session_state:
                    del st.session_state[key]

            st.session_state.app_stage = "setup"
            st.rerun()
