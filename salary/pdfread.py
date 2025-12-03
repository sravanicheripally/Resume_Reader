# -------------------------------------------------------------------------------------------------------
import re
import pdfplumber
import pandas as pd
import asyncio
from salary import docx_custom


# -------------------------------------------------------------
# TECHNOLOGIES (full list)
# -------------------------------------------------------------
from .tech_list import technologies     # Move list to separate file for clarity


# -------------------------------------------------------------
# ONLY FIELDS YOU WANT
# -------------------------------------------------------------
def extract_info(data):
    result = {
        "Name": None,
        "Email": None,
        "Phone": None,
        "Role": None,
        "Skills": []
    }

    if not isinstance(data, list):
        data = data.split("\n")

    # ---------------- Patterns ----------------
    phone_pattern = r"(?:\+\d{1,3}\s?)?\d{10}"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    # Explicit labels
    role_label_pattern = r"(designation|role|position|title)\s*[:\- ]\s*([A-Za-z][A-Za-z0-9 \-/()]+)"

    # Keywords of typical job titles
    role_keywords = r"(developer|engineer|manager|lead|analyst|architect|tester|consultant|administrator|specialist|devops|qa)"

    # Skills
    skills_pattern = r'\b(?:' + '|'.join(map(re.escape, technologies)) + r')\b'

    # ---------------- Extract Name (line 1 usually) ----------------
    if data:
        first = data[0].strip()
        if len(first) > 2 and len(first) < 50:
            result["Name"] = first

    skills_set = set()

    # ---------------- Loop through lines ----------------
    for idx, line in enumerate(data):
        clean = line.strip()

        # ---- Phone ----
        if not result["Phone"]:
            p = re.findall(phone_pattern, clean)
            if p:
                result["Phone"] = p[0]

        # ---- Email ----
        if not result["Email"]:
            em = re.findall(email_pattern, clean)
            if em:
                result["Email"] = em[0]

        # ---- STEP 1 — Explicit Role Labels (strongest match) ----
        if not result["Role"]:
            m = re.search(role_label_pattern, clean, re.IGNORECASE)
            if m:
                result["Role"] = m.group(2).strip()
                continue

        # ---- Skip bad lines for role ----
        if re.search(email_pattern, clean): continue
        if re.search(phone_pattern, clean): continue
        if "linkedin" in clean.lower(): continue
        if "github" in clean.lower(): continue
        if "summary" in clean.lower(): continue
        if "objective" in clean.lower(): continue
        if "experience" in clean.lower(): continue
        if "project" in clean.lower(): continue
        if re.search(r"\b(year|yrs|months)\b", clean.lower()): continue
        if len(clean) > 60: continue  # avoid paragraphs

        # ---- STEP 2 — Job keyword based role detection ----
        if re.search(role_keywords, clean, re.IGNORECASE):
            # Avoid capturing NAME again
            if clean.lower() != result["Name"].lower():
                result["Role"] = clean
                continue

        # ---- Skills ----
        skill_matches = re.findall(skills_pattern, clean, re.IGNORECASE)
        for s in skill_matches:
            skills_set.add(s.lower())

    # ---------------- Skills Finalize ----------------
    result["Skills"] = list(skills_set)

    return result


# -------------------------------------------------------------
# PDF PARSER
# -------------------------------------------------------------
async def extract_pdf(uploaded_file):
    uploaded_file.seek(0)
    with pdfplumber.open(uploaded_file) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""
    return [extract_info(text)]


# -------------------------------------------------------------
# DOCX PARSER
# -------------------------------------------------------------
async def extract_docx(uploaded_file):
    doc = docx_custom.opendocx(uploaded_file)
    lines = docx_custom.getdocumenttext(doc)
    return [extract_info(lines)]


# -------------------------------------------------------------
# EXCEL PARSER
# -------------------------------------------------------------
async def parse_excel(uploaded_file):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pd.read_excel, uploaded_file)
