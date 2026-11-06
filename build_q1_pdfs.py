import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        if self._pageNumber > 1:
            self.drawString(54, 750, "Voice of India: National Speaker Diarization Benchmark Specification")
            self.drawRightString(558, 750, "November 2026")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 36, "JOSH TALKS & AI4BHARAT — PUBLIC EVALUATION FRAMEWORK")
        self.drawRightString(558, 36, page_str)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_q1_methodology_pdf():
    pdf_path = "JoshTalks_Growth_Assessment/question_1/final_report/Q1_Methodology_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('T', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor("#0f172a"), spaceAfter=6)
    sub_style = ParagraphStyle('Sub', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#1e3a8a"), spaceAfter=12)
    h1_style = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor("#0f172a"), spaceBefore=12, spaceAfter=5, keepWithNext=True)
    h2_style = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor("#1e3a8a"), spaceBefore=8, spaceAfter=4, keepWithNext=True)
    body_style = ParagraphStyle('B', fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#334155"), spaceAfter=5)
    bullet_style = ParagraphStyle('Bul', parent=body_style, leftIndent=12, bulletIndent=4, spaceAfter=4)
    th_style = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=colors.white)
    td_style = ParagraphStyle('TD', fontName='Helvetica', fontSize=7, leading=9, textColor=colors.HexColor("#1e293b"))

    story = []
    story.append(Paragraph("Voice of India: National Speaker Diarization Benchmark", title_style))
    story.append(Paragraph("Comprehensive Evaluation Framework, Methodology Specification, and Indian Corpus Architecture", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=10))

    # Read markdown and parse key sections
    with open("JoshTalks_Growth_Assessment/question_1/methodology/Q1_Methodology_Report.md", "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")
    in_table = False
    table_rows = []

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        if line_s.startswith("# "):
            continue # already added title
        elif line_s.startswith("## "):
            story.append(Paragraph(line_s[3:], h1_style))
        elif line_s.startswith("### "):
            story.append(Paragraph(line_s[4:], h2_style))
        elif line_s.startswith("- ") or line_s.startswith("* "):
            story.append(Paragraph("&bull; " + line_s[2:], bullet_style))
        elif line_s.startswith("|"):
            # table row
            if "---" in line_s:
                continue
            parts = [p.strip() for p in line_s.split("|")[1:-1]]
            if not in_table:
                in_table = True
                table_rows = [parts]
            else:
                table_rows.append(parts)
        else:
            if in_table:
                # build table
                t_data = []
                for r_idx, row in enumerate(table_rows):
                    row_cells = []
                    for c_idx, cell in enumerate(row):
                        st = th_style if r_idx == 0 else td_style
                        row_cells.append(Paragraph(cell, st))
                    t_data.append(row_cells)
                # auto width
                num_cols = len(table_rows[0])
                w = 504.0 / num_cols
                t = Table(t_data, colWidths=[w]*num_cols)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                    ('TOPPADDING', (0, 0), (-1, -1), 2),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ]))
                story.append(t)
                story.append(Spacer(1, 6))
                in_table = False
                table_rows = []
            story.append(Paragraph(line_s, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Built Q1 Methodology PDF: {pdf_path}")

def build_q1_exec_summary_pdf():
    pdf_path = "JoshTalks_Growth_Assessment/question_1/executive_summary/Q1_Executive_Summary.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('T', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor("#0f172a"), spaceAfter=4)
    sub_style = ParagraphStyle('Sub', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#1e3a8a"), spaceAfter=10)
    h1_style = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor("#0f172a"), spaceBefore=8, spaceAfter=4, keepWithNext=True)
    body_style = ParagraphStyle('B', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#334155"), spaceAfter=6)
    bullet_style = ParagraphStyle('Bul', parent=body_style, leftIndent=12, bulletIndent=4, spaceAfter=4)

    story = []
    story.append(Paragraph("Executive Summary: Voice of India Diarization Benchmark", title_style))
    story.append(Paragraph("National Evaluation Standard & Public Leaderboard Architecture for Indian Conversational Speech", sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=10))

    with open("JoshTalks_Growth_Assessment/question_1/executive_summary/Q1_Executive_Summary.md", "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")
    for line in lines:
        line_s = line.strip()
        if not line_s or line_s.startswith("# "):
            continue
        if line_s.startswith("### "):
            story.append(Paragraph(line_s[4:], h1_style))
        elif line_s.startswith("- ") or line_s.startswith("* "):
            story.append(Paragraph("&bull; " + line_s[2:], bullet_style))
        elif not line_s.startswith("+--") and not line_s.startswith("|"):
            story.append(Paragraph(line_s, body_style))

    doc.build(story)
    print(f"Built Q1 Exec Summary PDF: {pdf_path}")

if __name__ == "__main__":
    build_q1_methodology_pdf()
    build_q1_exec_summary_pdf()

