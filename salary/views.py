from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os
import pandas as pd
import asyncio

from .pdfread import extract_docx, extract_pdf, parse_excel


# -------------------------------------------------------------
# SAVE RESUME
# -------------------------------------------------------------
def save_resume(uploaded_file, request):
    folder = os.path.join(settings.MEDIA_ROOT, "resumes")
    os.makedirs(folder, exist_ok=True)

    fs = FileSystemStorage(location=folder)
    filename = fs.save(uploaded_file.name, uploaded_file)
    return request.build_absolute_uri(settings.MEDIA_URL + "resumes/" + filename)


# -------------------------------------------------------------
# PROCESS EACH FILE
# -------------------------------------------------------------
async def process_file(uploaded_file, data, excel_frames, request):
    uploaded_file.seek(0)
    file_name = uploaded_file.name.lower()

    link = save_resume(uploaded_file, request)

    if file_name.endswith(".pdf"):
        rows = await extract_pdf(uploaded_file)

    elif file_name.endswith(".docx"):
        rows = await extract_docx(uploaded_file)

    elif file_name.endswith(".xlsx"):
        df = await parse_excel(uploaded_file)
        excel_frames.append(df)
        return

    else:
        print("⚠ Unsupported file:", file_name)
        return

    # Add resume link
    if rows:
        rows[0]["Resume_Link"] = link

    data.extend(rows)


# -------------------------------------------------------------
# MAIN VIEW
# -------------------------------------------------------------
async def process_salary(request):

    if request.method == "POST":

        files = request.FILES.getlist("files")
        folder = request.POST.get("folderName", "output")

        if not files:
            return HttpResponse("Please upload at least one file.")

        data = []
        excels = []
        tasks = [process_file(f, data, excels, request) for f in files]

        await asyncio.gather(*tasks)

        # If resume data exists
        if data:
            df = pd.DataFrame(data)
            df["Resume_Link"] = df["Resume_Link"].apply(
                lambda x: f'=HYPERLINK("{x}", "Open Resume")'
            )

            file_name = f"{folder}_resume_data.xlsx"
            df.to_excel(file_name, index=False)

        # If only excel files
        elif excels:
            merged = pd.concat(excels, ignore_index=True)
            merged.drop_duplicates(subset=["Email"], inplace=True)

            file_name = f"{folder}_merged_excel.xlsx"
            merged.to_excel(file_name, index=False)

        else:
            return HttpResponse("No valid data found in uploaded files.")

        with open(file_name, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = f"attachment; filename={file_name}"
            return response

    return render(request, "temp2.html")
