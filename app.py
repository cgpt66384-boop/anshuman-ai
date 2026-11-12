
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(
    page_title="ANSHUMAN AI",
    page_icon="🤖",
    layout="wide"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#101426,#191b35);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
[data-testid="stChatMessage"] {
    background: #222641;
    border-radius: 14px;
}
.stButton button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "generated_file" not in st.session_state:
    st.session_state.generated_file = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

# ---------- HEADER ----------
st.title("🤖 ANSHUMAN AI")
st.caption("Your personal AI workspace • Think • Create • Research • Automate")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("ANSHUMAN AI")
    st.write("Your personal workspace")

    st.divider()

    if st.button("➕ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.generated_file = None
        st.session_state.file_name = None
        st.rerun()

    st.subheader("Capabilities")
    st.write("📊 Excel generation")
    st.write("📝 Word documents")
    st.write("📽️ Presentations")
    st.write("📄 PDF workflows")
    st.write("🖼️ Image uploads")
    st.write("🧠 AI brain – coming next")

    st.divider()
    st.caption("ANSHUMAN AI • Version 0.1")

# ---------- FILE UPLOAD ----------
st.subheader("📎 Upload a file")

uploaded = st.file_uploader(
    "Upload an image, PDF or document",
    type=["png", "jpg", "jpeg", "pdf", "txt", "csv"]
)

if uploaded:
    st.success("File received: " + uploaded.name)

    if uploaded.type.startswith("image/"):
        st.image(uploaded, caption=uploaded.name, width=350)

    elif uploaded.type == "text/plain":
        st.text_area(
            "File contents",
            uploaded.getvalue().decode("utf-8", errors="replace"),
            height=150
        )

    elif uploaded.type == "application/pdf":
        st.info("PDF uploaded. PDF reading will be added in the next development stage.")

# ---------- FILE GENERATION ----------
def create_excel():
    data = pd.DataFrame({
        "Roll Number": range(1, 11),
        "Student Name": [f"Student {i}" for i in range(1, 11)],
        "Present": [0] * 10,
        "Absent": [0] * 10,
        "Attendance Percentage": ["0%"] * 10
    })

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(writer, index=False, sheet_name="Attendance")
        sheet = writer.sheets["Attendance"]
        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions

        for column in sheet.columns:
            letter = column[0].column_letter
            sheet.column_dimensions[letter].width = 23

    return output.getvalue()


def create_word():
    from docx import Document

    doc = Document()
    doc.add_heading("ANSHUMAN AI - New Document", 0)
    doc.add_paragraph("Document created using ANSHUMAN AI.")
    doc.add_paragraph(
        "Edit this document and add your required information."
    )

    output = BytesIO()
    doc.save(output)
    return output.getvalue()


def create_presentation():
    from pptx import Presentation

    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "ANSHUMAN AI Presentation"
    slide.placeholders[1].text = "Created with ANSHUMAN AI"

    output = BytesIO()
    prs.save(output)
    return output.getvalue()


def create_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(60, 780, "ANSHUMAN AI")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(60, 745, "Your document is ready.")
    pdf.save()

    return output.getvalue()


# ---------- INITIAL COMMAND SYSTEM ----------
def process_command(prompt):
    text = prompt.lower()

    if "excel" in text or "spreadsheet" in text:
        return (
            "I created a sample Excel attendance spreadsheet.",
            create_excel(),
            "ANSHUMAN_Attendance.xlsx"
        )

    if "word" in text or "document" in text:
        return (
            "I created a sample Word document.",
            create_word(),
            "ANSHUMAN_Document.docx"
        )

    if "powerpoint" in text or "presentation" in text:
        return (
            "I created a sample PowerPoint presentation.",
            create_presentation(),
            "ANSHUMAN_Presentation.pptx"
        )

    if "pdf" in text:
        return (
            "I created a sample PDF document.",
            create_pdf(),
            "ANSHUMAN_Document.pdf"
        )

    return (
        "I'm your ANSHUMAN AI starter. I can currently generate sample Excel, Word, PowerPoint and PDF files. More intelligent reasoning and task execution will be added in upcoming versions.",
        None,
        None
    )


# ---------- CHAT INTERFACE ----------
st.divider()
st.subheader("💬 Talk to ANSHUMAN AI")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Tell ANSHUMAN AI what you want it to do..."
)

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    response, file_data, file_name = process_command(prompt)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)

        if file_data:
            st.session_state.generated_file = file_data
            st.session_state.file_name = file_name

            st.download_button(
                "⬇️ Download your file",
                data=file_data,
                file_name=file_name,
                key="download_" + str(len(st.session_state.messages))
            )

# ---------- FOOTER ----------
st.divider()
st.caption(
    "ANSHUMAN AI © 2026 | Built for intelligent work and productivity"
)
