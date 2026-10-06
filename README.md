# InterviewIQ 🎯

### Adaptive AI Interviewer

InterviewIQ is an AI-powered personalized mock interview platform that analyzes a candidate's Resume and Job Description to conduct a role-specific, adaptive interview.

Instead of generating a fixed list of interview questions, InterviewIQ evaluates each response and dynamically adjusts the difficulty and focus of subsequent questions.

---

## 🚀 Live Demo

[Launch InterviewIQ](https://interviewiq-v2dmx6qyhk5nvyjpbibsk4.streamlit.app/)

---

## 🎯 Problem Statement

Traditional mock interview platforms often provide generic questions and static feedback.

Candidates need a more personalized practice environment that can:

- Understand their individual profile and experience
- Analyze the target Job Description
- Ask role-specific interview questions
- Evaluate responses systematically
- Adapt the interview based on previous performance
- Provide actionable feedback at the end

InterviewIQ addresses this problem through an AI-driven adaptive interview workflow.

---

## 💡 Key Features

### 1. Resume Analysis
Upload a candidate's Resume in PDF format.

### 2. Job Description Analysis
Upload the target Job Description in PDF format.

### 3. Role-Specific Interview
The candidate specifies the target role and receives questions aligned with the Resume and Job Description.

### 4. Adaptive Questioning
Interview difficulty progresses through three stages:

- **Warm-up Phase** — Questions 1–4
- **Core Assessment Phase** — Questions 5–8
- **Advanced Assessment Phase** — Questions 9–12

Subsequent questions are influenced by previous responses.

### 5. Structured AI Evaluation
Every answer is evaluated using five dimensions:

| Dimension | Weight |
|---|---:|
| Relevance | 25% |
| Accuracy | 30% |
| Depth | 20% |
| Communication | 15% |
| JD Alignment | 10% |

### 6. Performance Report
After 12 questions, InterviewIQ provides:

- Overall score
- Competency breakdown
- Question-wise feedback
- Interview readiness assessment
- Final recommendation
- Recommended next steps

### 7. AI Response Performance
The application also tracks:

- Number of AI calls
- Average response time
- Fastest response
- Slowest response
- Total Gemini processing time

---

## 🧠 How InterviewIQ Works

```text
Resume + Job Description
          ↓
    Profile Analysis
          ↓
  Target Role Analysis
          ↓
   Initial Question
          ↓
    Candidate Answer
          ↓
   AI Evaluation
          ↓
Adaptive Next Question
          ↓
    Candidate Answer
          ↓
        ...
          ↓
   Final Performance
        Report