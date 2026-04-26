import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SUMMARIZE_PROMPT = """You are an expert academic note-taker. Summarize the following lecture transcript into structured study notes.

Your output MUST follow this exact structure:

## Overview
Write 3-5 sentences describing what this lecture is about.

## Main Topics Covered
For each major topic, write a heading and bullet points explaining the key ideas.

## Key Definitions
List all important terms and their plain-English explanations.

## Important Concepts
List any formulas, algorithms, frameworks, or processes mentioned.

## Examples Discussed
List real examples the lecturer used to explain concepts.

## Quick Review
Write exactly 10 bullet points of the most important things to remember.

---
TRANSCRIPT:
{transcript}
---

Write the summary now. Be thorough but concise. Use academic language.
IMPORTANT: Always write your response in English, even if the transcript is in Urdu, Hindi, or any other language."""


def chunk_transcript(transcript: str, chunk_size: int = 12000, overlap: int = 500) -> list:
    words = transcript.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start = end - overlap
    return chunks


def merge_summaries(summaries: list) -> str:
    if len(summaries) == 1:
        return summaries[0]

    combined = "\n\n---PART BREAK---\n\n".join(summaries)
    merge_prompt = f"""You are merging multiple partial summaries of the same lecture into one coherent final summary.
Always write in English regardless of the original language.

Here are the partial summaries:
{combined}

Create one unified summary following this exact structure:

## Overview
3-5 sentences about the whole lecture.

## Main Topics Covered
All major topics combined and organized.

## Key Definitions
All terms from all parts combined.

## Important Concepts
All formulas, algorithms, frameworks combined.

## Examples Discussed
All examples combined.

## Quick Review
Exactly 10 bullet points of the most important things.

Write the merged summary now in English."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": merge_prompt}],
        max_tokens=4000
    )
    return response.choices[0].message.content


def summarize_transcript(transcript: str, word_count: int, custom_instructions: str = "") -> dict:
    try:
        prompt_template = SUMMARIZE_PROMPT
        if custom_instructions:
            prompt_template = SUMMARIZE_PROMPT + f"\n\nAdditional instructions: {custom_instructions}"

        if word_count > 15000:
            chunks = chunk_transcript(transcript)
            summaries = []
            for chunk in chunks:
                prompt = prompt_template.format(transcript=chunk)
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4000
                )
                summaries.append(response.choices[0].message.content)
            final_summary = merge_summaries(summaries)
        else:
            prompt = prompt_template.format(transcript=transcript)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000
            )
            final_summary = response.choices[0].message.content

        return {
            "success": True,
            "summary": final_summary
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Summarization failed: {str(e)}"
        }