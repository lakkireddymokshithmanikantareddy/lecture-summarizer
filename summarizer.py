"""
Gemini API integration for lecture summarization.

Uses the current google-genai SDK (>= 2.25.0) with the Interactions API
and model gemini-3.8-flash (gemini-1.5-flash is legacy/deprecated).
"""

import os
import re

from dotenv import load_dotenv

load_dotenv()


def _get_client():
    """Return an authenticated google-genai client."""
    from google import genai  # noqa: PLC0415

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY environment variable is not set. "
            "Copy .env.example to .env and add your key."
        )
    return genai.Client(api_key=api_key)


_PROMPT_TEMPLATE = """You are an expert academic tutor. A student has given you their lecture notes.
Produce a structured study summary in EXACTLY the following format (use these exact section headers):

## Key Concepts
- [bullet point 1]
- [bullet point 2]
(list the 5-10 most important concepts as bullet points)

## Important Definitions
[Term]: [definition]
[Term]: [definition]
(list 3-8 key terms and their definitions)

## Summary Paragraph
[Write 2-3 clear sentences summarising the lecture's main message]

## Possible Exam Questions
1. [question]
2. [question]
3. [question]
(list 3-5 likely exam questions based on the content)

---
LECTURE NOTES:
{text}
"""


def _parse_sections(raw: str) -> dict:
    """
    Parse the structured Gemini response into a Python dict.
    Returns keys: key_concepts, definitions, summary, exam_questions, raw.
    """

    def _between(text: str, start_header: str, end_headers: list) -> str:
        """Extract text between start_header and the first of end_headers."""
        pattern = re.compile(
            rf"##\s*{re.escape(start_header)}\s*\n(.*?)(?=##\s*(?:{'|'.join(re.escape(h) for h in end_headers)})|\Z)",
            re.DOTALL | re.IGNORECASE,
        )
        m = pattern.search(text)
        return m.group(1).strip() if m else ""

    all_headers = [
        "Key Concepts",
        "Important Definitions",
        "Summary Paragraph",
        "Possible Exam Questions",
    ]

    # --- Key Concepts ---
    kc_raw = _between(raw, "Key Concepts", all_headers[1:])
    key_concepts = [
        line.lstrip("-* \t").strip()
        for line in kc_raw.splitlines()
        if line.strip().lstrip("-* \t")
    ]

    # --- Definitions ---
    def_raw = _between(raw, "Important Definitions", all_headers[2:])
    definitions = {}
    for line in def_raw.splitlines():
        line = line.strip()
        if ":" in line:
            term, _, defn = line.partition(":")
            term = term.strip().strip("-* \t[]")
            defn = defn.strip().strip("[]")
            if term and defn:
                definitions[term] = defn

    # --- Summary Paragraph ---
    summary = _between(raw, "Summary Paragraph", all_headers[3:])
    summary = " ".join(summary.split())  # normalise whitespace

    # --- Exam Questions ---
    eq_raw = _between(raw, "Possible Exam Questions", [])
    exam_questions = []
    for line in eq_raw.splitlines():
        line = line.strip()
        # Strip leading numbering like "1." or "1)" or bullets
        line = re.sub(r"^(\d+[\.\)]|\-|\*)\s*", "", line)
        if line:
            exam_questions.append(line)

    return {
        "key_concepts": key_concepts,
        "definitions": definitions,
        "summary": summary,
        "exam_questions": exam_questions,
        "raw": raw,
    }


_PREFERRED_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.8-flash",
]


def summarize_text(text: str) -> dict:
    """
    Call the Gemini API to summarize lecture notes with automatic model fallback.

    Args:
        text: The raw lecture notes as a plain-text string.

    Returns:
        A dict with keys: key_concepts, definitions, summary, exam_questions, raw.
    """
    client = _get_client()
    prompt = _PROMPT_TEMPLATE.format(text=text)

    last_error = None
    raw_response = ""

    for model in _PREFERRED_MODELS:
        # Prioritize generate_content for fast, direct inferencing
        try:
            resp = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            raw_response = resp.text or ""
            if raw_response.strip():
                break
        except Exception as exc:  # noqa: BLE001
            last_error = exc

        # Fallback to interactions API if needed
        try:
            interaction = client.interactions.create(
                model=model,
                input=prompt,
                store=False,
            )
            raw_response = interaction.output_text or ""
            if raw_response.strip():
                break
        except Exception as exc:  # noqa: BLE001
            last_error = exc

    if not raw_response.strip():
        raise RuntimeError(
            f"All candidate Gemini models failed to summarize. Last error: {last_error}"
        )

    return _parse_sections(raw_response)


