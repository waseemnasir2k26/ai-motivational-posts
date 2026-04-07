"""
generate_pdf.py
---------------
Builds docs/HOW-TO-GUIDE.pdf — a shareable, visually-rich walkthrough of
how this repo was built with Claude Code, and how anyone can fork it.

Usage:
    python generate_pdf.py

Requires:
    pip install reportlab Pillow
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    PageBreak, Table, TableStyle, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

ROOT = Path(__file__).parent
OUT_PDF = ROOT / "docs" / "HOW-TO-GUIDE.pdf"
SAMPLE_IMG = ROOT / "output" / "images" / "quote_01.png"

# ---------- COLORS ----------
INK = colors.HexColor("#0a0a14")
ACCENT = colors.HexColor("#0084ff")
GREEN = colors.HexColor("#00c853")
GRAY = colors.HexColor("#5a6275")
LIGHT = colors.HexColor("#f4f5f8")


# ---------- STYLES ----------
def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="MegaTitle",
        fontName="Helvetica-Bold",
        fontSize=44,
        leading=50,
        textColor=INK,
        alignment=TA_CENTER,
        spaceAfter=18,
    ))
    styles.add(ParagraphStyle(
        name="Subtitle",
        fontName="Helvetica",
        fontSize=18,
        leading=24,
        textColor=GRAY,
        alignment=TA_CENTER,
        spaceAfter=24,
    ))
    styles.add(ParagraphStyle(
        name="SectionH",
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=INK,
        spaceBefore=20,
        spaceAfter=10,
    ))
    styles.add(ParagraphStyle(
        name="StepH",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=ACCENT,
        spaceBefore=14,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=11,
        leading=17,
        textColor=INK,
        spaceAfter=8,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="Mono",
        fontName="Courier",
        fontSize=9.5,
        leading=14,
        textColor=INK,
        backColor=LIGHT,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=6,
        spaceAfter=10,
        borderPadding=10,
    ))
    styles.add(ParagraphStyle(
        name="Pull",
        fontName="Helvetica-Oblique",
        fontSize=14,
        leading=20,
        textColor=GREEN,
        leftIndent=20,
        rightIndent=20,
        spaceBefore=10,
        spaceAfter=14,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="Caption",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=GRAY,
        alignment=TA_CENTER,
        spaceAfter=10,
    ))
    return styles


# ---------- BUILD ----------
def build():
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
        title="AI Motivational Posts — Built With Claude Code",
        author="Waseem Nasir / SkynetJoe",
    )

    s = make_styles()
    story = []

    # ---------- COVER ----------
    story.append(Spacer(1, 0.7 * inch))
    story.append(Paragraph("10 Motivational Posts.<br/>One Conversation.", s["MegaTitle"]))
    story.append(Paragraph(
        "How I built this entire pipeline with Claude Code &mdash; and how you can copy it in 60 seconds.",
        s["Subtitle"],
    ))

    if SAMPLE_IMG.exists():
        img = RLImage(str(SAMPLE_IMG), width=3.2 * inch, height=4 * inch)
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Paragraph("Sample output: 1080&times;1350 PNG, ready for Instagram, LinkedIn, X, TikTok.", s["Caption"]))

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        "By Waseem Nasir &middot; <font color='#0084ff'>github.com/waseemnasir2k26/ai-motivational-posts</font>",
        s["Caption"],
    ))
    story.append(PageBreak())

    # ---------- WHAT YOU GET ----------
    story.append(Paragraph("What you get", s["SectionH"]))
    story.append(Paragraph(
        "This repo collapses the entire &ldquo;motivational quote post&rdquo; pipeline into "
        "a single JSON file plus two Python scripts. No Canva, no Photoshop, no manual "
        "scheduling. Edit one file, run two commands, upload one CSV.",
        s["Body"],
    ))

    bullets = [
        ["10 ready-to-post quote cards", "1080x1350 PNG, Tommy Mello tweet style"],
        ["A 39-column GoHighLevel CSV", "Schedules every post across FB, IG, LinkedIn, YouTube Shorts, TikTok, Pinterest"],
        ["Data-driven JSON", "Edit one file to change author, quotes, captions, schedule"],
        ["Brand-consistent design", "Same avatar, layout, and color palette across all 10 cards"],
        ["This PDF guide", "Walks through the entire workflow"],
    ]
    table = Table(bullets, colWidths=[2.0 * inch, 4.0 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(table)

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "&ldquo;Most quote-creator tools take 20 minutes per post. This pipeline does 10 posts in 60 seconds.&rdquo;",
        s["Pull"],
    ))

    story.append(PageBreak())

    # ---------- HOW IT WAS BUILT ----------
    story.append(Paragraph("How Claude Code built this", s["SectionH"]))
    story.append(Paragraph(
        "Every file in this repo &mdash; the image generator, the CSV builder, the README, even this PDF "
        "&mdash; was produced inside a single Claude Code conversation. Below are the four prompts I "
        "actually used. Copy them, swap the niche, and you'll get your own version.",
        s["Body"],
    ))

    steps = [
        (
            "Step 1 &mdash; Draft the content",
            "&quot;Create 10 motivational quote ideas for [your niche] in a Tommy Mello tweet style. "
            "Each one needs a 1-2 sentence quote, a 4-line caption, and 10 mixed-tier hashtags. "
            "Show them in an HTML preview with my headshot.&quot;",
            "&rarr; Claude wrote preview.html. I reviewed all 10 in my browser and approved.",
        ),
        (
            "Step 2 &mdash; Render the images",
            "&quot;I approve these. Write a Python script using Pillow that reads a JSON file and renders "
            "each quote as a 1080x1350 PNG: white card, black top/bottom bars, circular avatar with "
            "green glow, blue verified badge next to my name, bold quote text auto-shrunk to fit.&quot;",
            "&rarr; Claude wrote generate_images.py. One run produced all 10 PNGs.",
        ),
        (
            "Step 3 &mdash; Build the GHL CSV",
            "&quot;Now write a Python script that reads the same JSON and outputs a GoHighLevel Advanced "
            "bulk-post CSV (39 columns, 2-row header). Schedule one post per day starting [date], "
            "using these times by weekday: Mon 9am, Tue 12pm, Wed 10am, Thu 2pm, Fri 5pm, Sat 11am, Sun 10am EST.&quot;",
            "&rarr; Claude wrote build_csv.py matching the exact GHL Advanced format.",
        ),
        (
            "Step 4 &mdash; Package and ship",
            "&quot;Refactor the whole thing into a clean public repo, write a README that tells the story, "
            "and generate a shareable PDF guide.&quot;",
            "&rarr; Claude built the folder structure, README, .gitignore, and this PDF.",
        ),
    ]

    for title, prompt, result in steps:
        story.append(Paragraph(title, s["StepH"]))
        story.append(Paragraph(prompt, s["Mono"]))
        story.append(Paragraph(result, s["Body"]))

    story.append(PageBreak())

    # ---------- QUICK START ----------
    story.append(Paragraph("Run it yourself in 60 seconds", s["SectionH"]))
    story.append(Paragraph(
        "Once you've forked or cloned the repo, the workflow is four commands:",
        s["Body"],
    ))

    quick_start = (
        "git clone https://github.com/waseemnasir2k26/ai-motivational-posts.git<br/>"
        "cd ai-motivational-posts<br/>"
        "pip install Pillow reportlab<br/>"
        "python generate_images.py     <font color='#5a6275'># makes 10 PNGs</font><br/>"
        "python build_csv.py           <font color='#5a6275'># makes the GHL CSV</font>"
    )
    story.append(Paragraph(quick_start, s["Mono"]))

    story.append(Paragraph("Then customize:", s["StepH"]))
    customize = [
        ("Change the quotes", "Edit posts.json &rarr; the posts array. 10 quotes total."),
        ("Change author identity", "Edit posts.json &rarr; the author block. Replace photo.png."),
        ("Change schedule", "Edit posts.json &rarr; schedule.start_date and times_by_weekday."),
        ("Change image hosting", "Edit build_csv.py &rarr; REPO_RAW_URL to your fork's raw URL."),
    ]
    table2 = Table(customize, colWidths=[1.8 * inch, 4.2 * inch])
    table2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.white),
    ]))
    story.append(table2)

    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Upload to GoHighLevel", s["StepH"]))
    story.append(Paragraph(
        "In your GHL workspace, go to <b>Marketing &rarr; Social Planner &rarr; Bulk Upload &rarr; Advanced</b>. "
        "Select <b>output/ghl-batch4-quotes.csv</b>. GHL will validate the 39 columns, then ask which "
        "social accounts to publish to. Pick all of them. Done.",
        s["Body"],
    ))

    story.append(PageBreak())

    # ---------- WHY THIS MATTERS ----------
    story.append(Paragraph("Why this matters", s["SectionH"]))
    story.append(Paragraph(
        "Most creators are stuck in a loop: open Canva, drag a template, retype the quote, export, "
        "rename the file, upload to a scheduler, set a date, click publish, repeat. Twenty minutes per post. "
        "Three hundred minutes for fifteen posts. That's a full workday burned on busywork.",
        s["Body"],
    ))
    story.append(Paragraph(
        "When the workflow lives in code &mdash; and the code is generated by Claude Code &mdash; "
        "the cost of a new batch drops to <b>seconds</b>. New niche? Edit posts.json. New brand? Swap photo.png. "
        "New schedule? Change one date. The repo does the rest.",
        s["Body"],
    ))
    story.append(Paragraph(
        "&ldquo;Don't trade time for money. Trade systems for freedom.&rdquo;",
        s["Pull"],
    ))
    story.append(Paragraph(
        "That's quote #4 in this batch. It's also why this repo exists.",
        s["Body"],
    ))

    # ---------- CTA ----------
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("Fork the repo. Ship your batch.", s["SectionH"]))
    story.append(Paragraph(
        "&rarr; <font color='#0084ff'><b>github.com/waseemnasir2k26/ai-motivational-posts</b></font>",
        s["Body"],
    ))
    story.append(Paragraph(
        "If this saved you time, share the repo and tag me. Let's flood the timeline with content built in minutes, not hours.",
        s["Body"],
    ))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Built by Waseem Nasir", s["StepH"]))
    story.append(Paragraph(
        "Founder of <b>SkynetJoe / Skynet Labs</b>. I build AI agents, automation systems, and revenue "
        "machines for agencies and startups.",
        s["Body"],
    ))
    story.append(Paragraph(
        "&middot; Web: <font color='#0084ff'>www.skynetjoe.com</font><br/>"
        "&middot; Personal: <font color='#0084ff'>www.waseemnasir.com</font><br/>"
        "&middot; 47 free tools: <font color='#0084ff'>skynetlabs-toolkit.vercel.app</font><br/>"
        "&middot; GitHub: <font color='#0084ff'>github.com/waseemnasir2k26</font>",
        s["Body"],
    ))

    doc.build(story)
    print(f"PDF written to {OUT_PDF}")


if __name__ == "__main__":
    build()
