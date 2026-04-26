import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

QUIZ_PROMPT = """You are an expert academic quiz creator. Based on the following lecture summary, create a comprehensive quiz.

Generate EXACTLY this structure — no more, no less:

## MULTIPLE CHOICE QUESTIONS

Q1. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q2. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q3. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q4. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q5. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q6. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q7. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q8. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q9. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

Q10. [Question text]
A) [Option]
B) [Option]
C) [Option]
D) [Option]
Answer: [A/B/C/D]

## SHORT ANSWER QUESTIONS

S1. [Question text]
Answer: [Detailed answer in 2-3 sentences]

S2. [Question text]
Answer: [Detailed answer in 2-3 sentences]

S3. [Question text]
Answer: [Detailed answer in 2-3 sentences]

S4. [Question text]
Answer: [Detailed answer in 2-3 sentences]

S5. [Question text]
Answer: [Detailed answer in 2-3 sentences]

---
LECTURE SUMMARY:
{summary}
---

Generate the quiz now. Make questions test real understanding, not just memorization."""


def generate_quiz(summary: str) -> dict:
    try:
        prompt = QUIZ_PROMPT.format(summary=summary)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        quiz_text = response.choices[0].message.content
        return {
            "success": True,
            "quiz": quiz_text
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Quiz generation failed: {str(e)}"
        }


def parse_quiz(quiz_text: str) -> dict:
    """Parse quiz text into MCQs and short answers separately."""
    mcq_section = ""
    short_section = ""

    if "## SHORT ANSWER QUESTIONS" in quiz_text:
        parts = quiz_text.split("## SHORT ANSWER QUESTIONS")
        mcq_section = parts[0].replace("## MULTIPLE CHOICE QUESTIONS", "").strip()
        short_section = parts[1].strip()
    else:
        mcq_section = quiz_text

    return {
        "mcq": mcq_section,
        "short": short_section
    }