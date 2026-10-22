"""
Lecture Summarizer - Flask Application
University student tool for AI-powered lecture note summarization.
"""

import os
import uuid
import time

from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

from summarizer import summarize_text
from logger import log_session, get_logs

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-me")

# Ensure required directories exist
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extract_pdf_text(file_path: str) -> str:
    """Extract plain text from a PDF file using PyPDF2."""
    try:
        import PyPDF2  # noqa: PLC0415

        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Failed to extract text from PDF: {exc}") from exc


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    # --- POST: handle either text paste or PDF upload ---
    notes_text = request.form.get("notes_text", "").strip()
    pdf_file = request.files.get("pdf_file")

    input_text = ""

    if pdf_file and pdf_file.filename:
        # Save the upload temporarily
        safe_name = f"{uuid.uuid4().hex}.pdf"
        temp_path = os.path.join(UPLOAD_FOLDER, safe_name)
        try:
            pdf_file.save(temp_path)
            input_text = extract_pdf_text(temp_path)
        except RuntimeError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    elif notes_text:
        input_text = notes_text
    else:
        flash("Please paste some lecture notes or upload a PDF file.", "error")
        return redirect(url_for("index"))

    if not input_text.strip():
        flash("Could not extract any text. Please check your input and try again.", "error")
        return redirect(url_for("index"))

    # --- Summarize ---
    session_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        result = summarize_text(input_text)
    except Exception as exc:  # noqa: BLE001
        flash(f"Summarization failed: {exc}", "error")
        return redirect(url_for("index"))

    processing_seconds = round(time.time() - start_time, 2)

    # --- Log the session ---
    log_session(
        session_id=session_id,
        input_chars=len(input_text),
        processing_seconds=processing_seconds,
    )

    return render_template(
        "summary.html",
        result=result,
        session_id=session_id,
        input_chars=len(input_text),
        processing_seconds=processing_seconds,
    )


@app.route("/logs")
def logs():
    all_logs = get_logs()
    return render_template("logs.html", logs=all_logs)


if __name__ == "__main__":
    app.run(debug=True)
