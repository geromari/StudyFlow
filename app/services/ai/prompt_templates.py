"""AI system prompts and template formatting."""

STUDY_ASSISTANT_SYSTEM_PROMPT = """You are StudyFlow, an elite personal AI study assistant and tutor for students.
Your mission is to make learning enjoyable, effective, and crystal-clear.

Guidelines:
- Explain concepts clearly using structured formatting, bullet points, and intuitive analogies.
- Tailor explanations to the requested language (Uzbek, English, or Russian).
- Be supportive, encouraging, and academically accurate.
- When asked to explain step-by-step, number each step cleanly.
- When generating study notes, use headings, key takeaways, and flashcard-style summaries.
- Keep answers concise and avoid rambling.
"""

MODE_PROMPTS = {
    "explain": "Explain the following topic simply and clearly, with intuitive real-world analogies: ",
    "summarize": "Provide a concise, high-yield summary highlighting the most critical key points of: ",
    "examples": "Provide practical, step-by-step examples demonstrating the concepts of: ",
    "study_notes": "Generate structured, high-yield study notes with key terms and bullet points for: ",
    "step_by_step": "Explain how to solve or understand this step-by-step with clear reasoning: ",
}

QUIZ_GENERATION_PROMPT = """Generate a multiple-choice quiz with {count} questions on the subject '{subject}' with '{difficulty}' difficulty.
Language of the quiz must be: {language}.

Return ONLY valid JSON matching this exact array structure:
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct_option": "A",
    "explanation": "Brief explanation of why A is correct."
  }}
]
Do not include any conversational filler, markdown fences, or extra text outside the JSON array.
"""

STUDY_PLAN_GENERATION_PROMPT = """Create a balanced, realistic daily study plan for a student.
Goal: {goal}
Daily Available Study Time: {target_minutes} minutes
Subjects to cover: {subjects}
Language: {language}

Return ONLY a valid JSON array of tasks with this format:
[
  {{
    "title": "Study task title",
    "scheduled_time": "09:00",
    "duration_minutes": 20,
    "subject": "Subject name"
  }}
]
Distribute the time logically so the sum of duration_minutes is approximately {target_minutes} minutes.
"""

DOCUMENT_QA_PROMPT = """You are answering questions based on the following document excerpt.
DOCUMENT CONTENT:
---
{document_excerpt}
---

USER QUESTION: {question}

Answer the user's question clearly, accurately, and strictly using the document context where applicable in {language}.
"""

DOCUMENT_SUMMARY_PROMPT = """Please provide a structured, executive summary of the following document excerpt in {language}.
Include:
1. Main Theme / Topic
2. Key Findings or Concepts (bullet points)
3. Essential Takeaways

DOCUMENT CONTENT:
---
{document_excerpt}
---
"""
