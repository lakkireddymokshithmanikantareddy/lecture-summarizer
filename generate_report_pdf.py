import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_OUTPUT = r"C:\Users\saipa\.gemini\antigravity\scratch\lecture-summarizer\Lecture_Summarizer_Project_Report.pdf"
LOGO_PATH = r"C:\Users\saipa\.gemini\antigravity\scratch\lecture-summarizer\pdf_assets\p1_0_X4.png"

PAGE_WIDTH, PAGE_HEIGHT = A4

class NumberedCanvas(canvas.Canvas):
    """Adds header (logo + faculty) and footer page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # Header on all pages
        if os.path.exists(LOGO_PATH):
            self.drawImage(LOGO_PATH, 42, PAGE_HEIGHT - 62, width=125, height=42, preserveAspectRatio=True, mask='auto')

        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(colors.HexColor("#1A202C"))
        self.drawRightString(PAGE_WIDTH - 42, PAGE_HEIGHT - 38, "Faculty of Engineering and Technology")
        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(colors.HexColor("#2D3748"))
        self.drawRightString(PAGE_WIDTH - 42, PAGE_HEIGHT - 50, "Department of CSE – AI, ML and DS")

        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(42, PAGE_HEIGHT - 68, PAGE_WIDTH - 42, PAGE_HEIGHT - 68)

        # Footer on pages >= 2
        if self._pageNumber >= 2:
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(42, 38, PAGE_WIDTH - 42, 38)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#718096"))
            self.drawString(42, 26, "AI-Assisted Web Application Project | Semester 3 CSE (AI/ML)")
            page_text = f"Page {self._pageNumber} of {total_pages}"
            self.drawRightString(PAGE_WIDTH - 42, 26, page_text)


def create_project_report():
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=76,
        bottomMargin=46,
    )

    styles = getSampleStyleSheet()

    title_main = ParagraphStyle(
        'TitleMain',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#1A365D"),
    )

    title_sub = ParagraphStyle(
        'TitleSub',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        alignment=1,
        textColor=colors.HexColor("#2B6CB0"),
    )

    h1_style = ParagraphStyle(
        'H1Style',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=5,
        spaceAfter=2,
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        fontName='Helvetica',
        fontSize=8.1,
        leading=11.2,
        textColor=colors.HexColor("#2D3748"),
        alignment=4,
        spaceAfter=2,
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1A365D"),
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.8,
        textColor=colors.HexColor("#2D3748"),
    )

    prompt_cell = ParagraphStyle(
        'PromptCell',
        fontName='Courier-Oblique',
        fontSize=7.2,
        leading=9.4,
        textColor=colors.HexColor("#1A202C"),
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1A202C"),
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 45))
    story.append(Paragraph("PROJECT REPORT", title_main))
    story.append(Spacer(1, 8))
    story.append(Paragraph("AI-Assisted Web Application Project", title_sub))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Semester 3 – CSE (AI/ML)", ParagraphStyle('Sem', fontName='Helvetica', fontSize=11, alignment=1, textColor=colors.HexColor("#4A5568"))))
    
    story.append(Spacer(1, 70))
    story.append(Paragraph("Project Title", ParagraphStyle('ProjLabel', fontName='Helvetica-Bold', fontSize=11.5, alignment=1, textColor=colors.HexColor("#718096"))))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Lecture Summarizer — AI-Powered Study Assistant", ParagraphStyle('ProjTitle', fontName='Helvetica-Bold', fontSize=15, leading=19, alignment=1, textColor=colors.HexColor("#2B6CB0"))))
    
    story.append(Spacer(1, 90))
    story.append(Paragraph("Submitted by", ParagraphStyle('SubBy', fontName='Helvetica-Bold', fontSize=11.5, alignment=1, textColor=colors.HexColor("#2D3748"))))
    story.append(Spacer(1, 14))

    sub_table_data = [
        [Paragraph("Student Name:", meta_label), Paragraph("Lakkireddy Mokshith Manikanta Reddy", meta_val)],
        [Paragraph("Enrollment No.:", meta_label), Paragraph("____________________________________________", meta_val)],
        [Paragraph("Division:", meta_label), Paragraph("____________________________________________", meta_val)],
    ]
    t_sub = Table(sub_table_data, colWidths=[110, 310])
    t_sub.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sub)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("Contents", title_main))
    story.append(Spacer(1, 25))

    toc_data = [
        [Paragraph("<b>1. Introduction</b>", body_style), Paragraph("3", body_style)],
        [Paragraph("<b>2. Target User</b>", body_style), Paragraph("3", body_style)],
        [Paragraph("<b>3. Tools Used</b>", body_style), Paragraph("3", body_style)],
        [Paragraph("<b>4. Prompt Engineering Process</b>", body_style), Paragraph("3", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Idea / Problem Analysis", body_style), Paragraph("3", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Requirements / Features", body_style), Paragraph("3", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 UI / Layout Design", body_style), Paragraph("3", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Code Generation", body_style), Paragraph("3", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Testing", body_style), Paragraph("3", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Debugging and Improvement", body_style), Paragraph("3", body_style)],
        [Paragraph("<b>5. Application Design and Development</b>", body_style), Paragraph("4", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 System Architecture Flow", body_style), Paragraph("4", body_style)],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 UI Components & Page Structure", body_style), Paragraph("4", body_style)],
        [Paragraph("<b>6. Final Application</b>", body_style), Paragraph("4", body_style)],
        [Paragraph("<b>7. Conclusion</b>", body_style), Paragraph("4", body_style)],
    ]
    t_toc = Table(toc_data, colWidths=[430, 80])
    t_toc.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(t_toc)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: SECTIONS 1 - 4
    # =========================================================================
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "During exam preparation and internal assessments, college students face the challenge of reviewing 40 to 60 dense slide decks per lecture. Reading through raw slides takes hours, and during fast-paced revision, critical definitions and exam-relevant concepts are easily missed. Standard text summarizers generate unstructured paragraphs without categorizing insights into a format suitable for active study.",
        body_style
    ))
    story.append(Paragraph(
        "To address this issue, I developed <b>Lecture Summarizer</b>, a Flask web application that takes either pasted notes or uploaded PDF slides and converts them into a 4-part structured study guide: Key Concepts, Definitions, Summary, and Exam Questions. Prompt engineering and AI assistance were utilized across all phases, including requirement scoping, UI styling, and multi-model failover debugging.",
        body_style
    ))

    story.append(Paragraph("2. Target User", h1_style))
    story.append(Paragraph(
        "The primary users are <b>undergraduate university students</b> (especially in engineering and sciences) requiring rapid, structured revision before tests. Secondary users include <b>Teaching Assistants and lecturers</b> who need to prepare quick recap handouts and sample quiz questions from syllabus materials without manual formatting.",
        body_style
    ))

    story.append(Paragraph("3. Tools Used", h1_style))
    story.append(Paragraph(
        "• <b>Stack:</b> Python 3.14, Flask 3.1 (backend web server), PyPDF2 3.0 (PDF text extraction), python-dotenv (environment variables), HTML5/CSS3 (responsive card layout with Inter font).<br/>"
        "• <b>AI Inference:</b> Google Gemini API via <code>google-genai</code> SDK, with a multi-model fallback engine (<code>gemini-3.5-flash-lite</code>, <code>gemini-flash-lite-latest</code>, <code>gemini-3.8-flash</code>).<br/>"
        "• <b>AI-Assisted Tools:</b> Antigravity Agent tools for prompt design, code scaffolding, automated testing, and live debugging.",
        body_style
    ))

    story.append(Paragraph("4. Prompt Engineering Process", h1_style))
    story.append(Paragraph(
        "The application was built iteratively using targeted prompt engineering at each stage:",
        body_style
    ))

    prompt_table_data = [
        [
            Paragraph("<b>Phase & Purpose</b>", table_header),
            Paragraph("<b>Engineered Prompt & Implementation Strategy</b>", table_header)
        ],
        [
            Paragraph("<b>4.1 Idea / Problem Analysis</b><br/><i>Purpose: Brainstorm realistic, high-impact college project concepts.</i>", table_cell),
            Paragraph("\"Give me simple ideas for a project that is useful to a university student. Suggest options across study productivity and campus life, and point out which one is best suited for an AI web app demo.\"", prompt_cell)
        ],
        [
            Paragraph("<b>4.2 Requirements & Features</b><br/><i>Purpose: Define functional architecture and output format constraints.</i>", table_cell),
            Paragraph("\"I want to build a Lecture Summarizer web app using Python Flask and Google Gemini API. It should accept pasted text or uploaded PDF files and return four specific sections: Key Concepts, Definitions, Summary, and Exam Questions. Also include session logging.\"", prompt_cell)
        ],
        [
            Paragraph("<b>4.3 UI / Layout Design</b><br/><i>Purpose: Create a distraction-free, tabbed academic interface.</i>", table_cell),
            Paragraph("\"Write an HTML/CSS UI with an academic blue theme. Use a two-tab interface on the home page: Tab 1 for typing/pasting text, Tab 2 for uploading a PDF. Render results in 4 separate visual cards with a session metadata strip showing execution latency.\"", prompt_cell)
        ],
        [
            Paragraph("<b>4.4 Code Generation</b><br/><i>Purpose: Enforce rigid markdown delimiters for deterministic regex parsing.</i>", table_cell),
            Paragraph("\"Write summarizer.py using google-genai SDK. Instruct the model to strictly output exact headers: '## Key Concepts', '## Important Definitions', '## Summary Paragraph', and '## Possible Exam Questions'. Write a parser that splits the response into a structured dict.\"", prompt_cell)
        ],
        [
            Paragraph("<b>4.5 Testing</b><br/><i>Purpose: Programmatically verify endpoint status codes and session logs.</i>", table_cell),
            Paragraph("\"Write a Python test script using Flask test_client that sends sample operating systems lecture notes to POST / and asserts that all four study sections are returned with an HTTP 200 status code.\"", prompt_cell)
        ],
        [
            Paragraph("<b>4.6 Debugging & Improvement</b><br/><i>Purpose: Overcome transient 503 errors and sanitize bracketed terms.</i>", table_cell),
            Paragraph("\"The Gemini free tier occasionally returns 503 UNAVAILABLE on gemini-3.8-flash due to traffic spikes. Update summarizer.py to automatically fallback through candidate models: gemini-3.5-flash-lite, gemini-flash-lite-latest, and gemini-3.8-flash. Also strip square brackets from terms.\"", prompt_cell)
        ],
    ]

    t_prompts = Table(prompt_table_data, colWidths=[175, 335])
    t_prompts.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_prompts)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SECTIONS 5 - 7
    # =========================================================================
    story.append(Paragraph("5. Application Design and Development", h1_style))
    story.append(Paragraph(
        "The application employs a lightweight modular structure with clean separation of concerns between routing (<code>app.py</code>), PDF buffer processing (<code>PyPDF2</code>), AI failover summarization (<code>summarizer.py</code>), and session logging (<code>logger.py</code>).",
        body_style
    ))

    arch_box_data = [
        [Paragraph(
            "<b>System Architecture & Data Flow:</b><br/>"
            "<code>User (Browser) ➔ [Paste Text / Upload PDF] ➔ PyPDF2 Text Extraction<br/>"
            "➔ Gemini Multi-Model Failover Engine [gemini-3.5-flash-lite / flash-lite-latest / 3.8-flash]<br/>"
            "➔ Deterministic Regex Section Parser ➔ Render 4 Study Cards (summary.html)<br/>"
            "➔ Session Telemetry Logger (logs/sessions.json)</code>",
            ParagraphStyle('Arch', fontName='Courier', fontSize=7.4, leading=10.5, textColor=colors.HexColor("#1A365D"))
        )]
    ]
    t_arch = Table(arch_box_data, colWidths=[510])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#BEE3F8")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>UI Components & Navigation Flow:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor("#2D3748"))))
    story.append(Paragraph(
        "• <b>Home Page (<code>/</code>):</b> Academic header with brand navigation, dual-tab card allowing users to switch between pasting raw notes and uploading PDF slides.<br/>"
        "• <b>Summary Results Page (<code>/</code> POST):</b> Renders a metadata strip (Session ID, characters analyzed, inference time in seconds) and four distinct visual cards: <i>Key Concepts</i> (bullet points), <i>Important Definitions</i> (term and definition pairs), <i>Summary Paragraph</i> (executive overview), and <i>Possible Exam Questions</i> (numbered questions for self-assessment). Includes an expandable raw response toggle.<br/>"
        "• <b>Session History Page (<code>/logs</code>):</b> Tabular audit log displaying timestamped records of past summarizations with character counts and processing latencies.",
        body_style
    ))

    story.append(Spacer(1, 3))
    story.append(Paragraph("6. Final Application", h1_style))
    story.append(Paragraph(
        "The completed application is running locally and verified through automated end-to-end tests. Across sample test cases (including Operating Systems virtual memory notes and Computer Networks TCP/UDP slides), the system achieved an average summarization latency of 4 to 8 seconds with zero unhandled exceptions.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Key Working Features:</b> Robust PDF text extraction, resilient multi-model failover ensuring uptime during API demand spikes, deterministic structured parsing, and persistent JSON telemetry.<br/>"
        "• <b>GitHub Repository Link:</b> <u>https://github.com/lakkireddymokshithmanikantareddy/lecture-summarizer</u>",
        body_style
    ))

    story.append(Spacer(1, 3))
    story.append(Paragraph("7. Conclusion", h1_style))
    story.append(Paragraph(
        "<b>Project Summary:</b> This project demonstrated the successful end-to-end development of an AI-assisted web utility addressing an authentic student problem. By combining a lightweight Flask backend with engineered prompt templates, unstructured lecture notes are reliably transformed into actionable revision study guides.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Role of AI:</b> Generative AI functioned both as the runtime processing brain (via Gemini models) and as a pair-programming collaborator across the development lifecycle—accelerating prototyping, generating test harnesses, and resolving deployment bottlenecks.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Future Scope:</b> Planned future enhancements include: (1) Export functionality enabling one-click download of generated study sheets as Markdown or styled PDFs, (2) Audio lecture transcription to summarize classroom recordings directly, and (3) An interactive quiz mode converting extracted definitions and exam questions into self-grading digital flashcards.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Report PDF generated successfully at:", PDF_OUTPUT)

if __name__ == "__main__":
    create_project_report()
