# from django.shortcuts import render, HttpResponse
# from django.http import HttpResponse
# from .pdfread import extract_pdf_data, extract_text_from_docx
# import re
# import asyncio
# import pandas as pd
# import os

# def NameFile(file):
#     name_match = re.search(r'_(.*?)\[\d+y_\d+m\]', file)
#     if name_match:
#         return name_match.group(1)
#     else:
#         return file

# def ExperienceFile(file):
#     exp_match = re.search(r'\d+y_\d+m', file)
#     if exp_match:
#         return exp_match.group(0)
#     else:
#         return None

# duplicates_count = 0
# def findunique(ls, op, file, folder_name):
#     global duplicates_count
#     items = list(op[0].items())
#     items.insert(0, ("NamefromFile", NameFile(file)))
#     items.insert(7, ("Exp_File", ExperienceFile(file)))
#     items.insert(8, ("FolderName", folder_name))  # Add Folder Name
#     op[0] = dict(items)
#     if ls is not None:
#         for i in ls:
#             if i['Email_id'] == op[0]['Email_id']:
#                 duplicates_count += 1
#                 return []
#     return op

# async def process_file(uploaded_file, data, dfs, folder_name):
#     fileName = uploaded_file.name
#     if fileName.endswith(".pdf"):
#         op = await extract_pdf_data(uploaded_file)
#         data.extend(findunique(data, op, fileName, folder_name))

#     elif fileName.endswith(".docx"):
#         op = await extract_text_from_docx(uploaded_file)
#         data.extend(findunique(data, op, fileName, folder_name))

#     elif fileName.endswith(".xlsx"):
#         df = await read_excel(uploaded_file)
#         dfs.append(df)

# async def read_excel(file):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, pd.read_excel, file)

# # @timecalculator
# async def process_salary(request):
#     if request.method == 'POST':
#         uploaded_files = request.FILES.getlist('files')
#         folder_name = request.POST.get('folderName', 'default_folder')
        
#         if not uploaded_files:
#             return HttpResponse("Please choose at least one file......!!")
        
#         data = []
#         dfs = []
#         tasks = []

#         for uploaded_file in uploaded_files:
#             tasks.append(process_file(uploaded_file, data, dfs, folder_name))

#         await asyncio.gather(*tasks)

#         excel_file = 'empty.xlsx'
#         try:
#             if data:
#                 df = pd.DataFrame(data)
#                 excel_file = f'{folder_name}_employee_resumes_data.xlsx'
#                 df.to_excel(excel_file, index=False)
#             elif dfs:
#                 merged_df = pd.concat(dfs, ignore_index=True)
#                 merged_df = merged_df.drop_duplicates(subset=['Email_id'])
#                 excel_file = f'{folder_name}_merged_excels.xlsx'
#                 merged_df.to_excel(excel_file, index=False)
#             with open(excel_file, 'rb') as fh:
#                 response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#                 response['Content-Disposition'] = f'inline; filename={excel_file}'
#                 global duplicates_count
#                 print('duplicates', duplicates_count)
#                 duplicates_count = 0
#                 return response
#         except FileNotFoundError:
#             return HttpResponse("Please choose at least one file......!!")
#         except Exception as e:
#             print(f"An error occurred: {e}")
#     return render(request, 'temp2.html')



# from django.shortcuts import render, HttpResponse
# from django.http import HttpResponse
# from .pdfread import extract_pdf_data, extract_text_from_docx
# import re
# import asyncio
# import pandas as pd
# import os

# def NameFile(file):
#     name_match = re.search(r'_(.*?)\[\d+y_\d+m\]', file)
#     if name_match:
#         return name_match.group(1)
#     else:
#         return file

# def ExperienceFile(file):
#     exp_match = re.search(r'\d+y_\d+m', file)
#     if exp_match:
#         return exp_match.group(0)
#     else:
#         return None

# duplicates_count = 0

# def findunique(ls, op, file, folder_name):
#     global duplicates_count
#     items = list(op[0].items())
#     items.insert(0, ("NamefromFile", NameFile(file)))
#     items.insert(7, ("Exp_File", ExperienceFile(file)))
#     items.insert(8, ("FolderName", folder_name))  # Add Folder Name
#     op[0] = dict(items)
#     if ls is not None:
#         for i in ls:
#             if i['Email_id'] == op[0]['Email_id']:
#                 duplicates_count += 1
#                 return []
#     return op

# # async def process_file(uploaded_file, data, dfs, folder_name):
# #     fileName = uploaded_file.name
# #     if fileName.endswith(".pdf"):
# #         op = await extract_pdf_data(uploaded_file)
# #         data.extend(findunique(data, op, fileName, folder_name))

# #     elif fileName.endswith(".docx") or fileName.endswith(".doc"):
# #         op = await extract_text_from_docx(uploaded_file)
# #         data.extend(findunique(data, op, fileName, folder_name))

# #     elif fileName.endswith(".xlsx"):
# #         df = await read_excel(uploaded_file)
# #         dfs.append(df)

# from zipfile import BadZipFile

# async def process_file(uploaded_file, data, dfs, folder_name, request):
#     fileName = uploaded_file.name

#     # 1. Save resume in /media/resumes/ and generate public URL
#     resume_link = save_resume_locally(uploaded_file, request)

#     try:
#         # 2. Extract content from resume
#         if fileName.endswith(".pdf"):
#             op = await extract_pdf_data(uploaded_file)

#         elif fileName.endswith(".docx") or fileName.endswith(".doc"):
#             op = await extract_text_from_docx(uploaded_file)

#         elif fileName.endswith(".xlsx"):
#             df = await read_excel(uploaded_file)
#             dfs.append(df)
#             return

#         else:
#             print(f"Unsupported file format: {fileName}")
#             return

#         # 3. Add Resume_link ONLY once
#         op[0]["Resume_Link"] = resume_link

#         # 4. Insert final record into output list
#         data.extend(findunique(data, op, fileName, folder_name))

#     except Exception as e:
#         print(f"Error processing file '{fileName}': {str(e)}")



# async def read_excel(file):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, pd.read_excel, file)





# # @timecalculator
# async def process_salary(request):
#     if request.method == 'POST':
#         uploaded_files = request.FILES.getlist('files')
#         folder_name = request.POST.get('folderName', 'default_folder')
        
#         if not uploaded_files:
#             return HttpResponse("Please choose at least one file......!!")
        
#         data = []
#         dfs = []
#         tasks = []

#         for uploaded_file in uploaded_files:
#             tasks.append(process_file(uploaded_file, data, dfs, folder_name, request))

#         await asyncio.gather(*tasks)

#         excel_file = 'empty.xlsx'
#         try:
#             if data:
#                 df = pd.DataFrame(data)

#                 # 🔥 Convert Resume_Link to a clickable hyperlink
#                 if "Resume_Link" in df.columns:
#                     df["Resume_Link"] = df["Resume_Link"].apply(
#                         lambda x: f'=HYPERLINK("{x}", "Open Resume")'
#                     )

#                 excel_file = f'{folder_name}_employee_resumes_data.xlsx'
#                 df.to_excel(excel_file, index=False)

#             elif dfs:
#                 merged_df = pd.concat(dfs, ignore_index=True)
#                 merged_df = merged_df.drop_duplicates(subset=['Email_id'])
#                 excel_file = f'{folder_name}_merged_excels.xlsx'
#                 merged_df.to_excel(excel_file, index=False)
#             with open(excel_file, 'rb') as fh:
#                 response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#                 response['Content-Disposition'] = f'inline; filename={excel_file}'
#                 global duplicates_count
#                 print('duplicates', duplicates_count)
#                 duplicates_count = 0
#                 return response
#         except FileNotFoundError:
#             return HttpResponse("Please choose at least one file......!!")
#         except Exception as e:
#             print(f"An error occurred: {e}")
#     return render(request, 'temp2.html')




# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
# import os

# def save_resume_locally(uploaded_file, request):
#     from django.conf import settings
#     from django.core.files.storage import FileSystemStorage
#     import os

#     # Create folder /media/resumes/
#     resume_folder = os.path.join(settings.MEDIA_ROOT, "resumes")
#     os.makedirs(resume_folder, exist_ok=True)

#     # Save file
#     fs = FileSystemStorage(location=resume_folder)
#     filename = fs.save(uploaded_file.name, uploaded_file)

#     # Build full absolute URL
#     file_url = request.build_absolute_uri(settings.MEDIA_URL + "resumes/" + filename)

#     return file_url

# ---------------------------------------------------------------------------

from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
import re
import pdfplumber
import pandas as pd
import asyncio
import tempfile

from .pdfread import extract_text_from_docx   # keep your docx processor
from zipfile import BadZipFile


# -------------------------------------------------------------
# 🔍 FILENAME HELPERS
# -------------------------------------------------------------
def NameFile(file):
    match = re.search(r'_(.*?)\[\d+y_\d+m\]', file)
    return match.group(1) if match else file

def ExperienceFile(file):
    match = re.search(r'\d+y_\d+m', file)
    return match.group(0) if match else None


# -------------------------------------------------------------
# 🔍 DUPLICATE CHECKING
# -------------------------------------------------------------
duplicates_count = 0

def findunique(existing_list, op, file, folder):
    """Avoid duplicate Email IDs."""
    global duplicates_count

    items = list(op[0].items())
    items.insert(0, ("NamefromFile", NameFile(file)))
    items.insert(7, ("Exp_File", ExperienceFile(file)))
    items.insert(8, ("FolderName", folder))
    op[0] = dict(items)

    if existing_list:
        for row in existing_list:
            if row["Email_id"] == op[0]["Email_id"]:
                duplicates_count += 1
                return []  # ignore duplicate

    return op


# -------------------------------------------------------------
# 📁 SAVE RESUME LOCALLY & GENERATE PUBLIC URL
# -------------------------------------------------------------
def save_resume_locally(uploaded_file, request):
    resume_folder = os.path.join(settings.MEDIA_ROOT, "resumes")
    os.makedirs(resume_folder, exist_ok=True)

    fs = FileSystemStorage(location=resume_folder)
    filename = fs.save(uploaded_file.name, uploaded_file)

    file_url = request.build_absolute_uri(settings.MEDIA_URL + "resumes/" + filename)
    return file_url


# -------------------------------------------------------------
# 📄 PDF EXTRACTOR — FIXED & CLEAN
# -------------------------------------------------------------
async def extract_pdf_data(uploaded_file):
    """Reads PDF safely with pdfplumber."""

    uploaded_file.seek(0)   # ★ CRITICAL FIX ★
    salary_data = []

    with pdfplumber.open(uploaded_file) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""   # avoid None → ""
        extract_dic = extract_info(text)
        salary_data.append(extract_dic)

    return salary_data


# -------------------------------------------------------------
# 📘 DOCX EXTRACTOR
# -------------------------------------------------------------
async def extract_text_from_docx_file(file):
    op = await extract_text_from_docx(file)  # your custom handler
    return op


# -------------------------------------------------------------
# 📊 XLSX READER
# -------------------------------------------------------------
async def read_excel(file):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pd.read_excel, file)


# -------------------------------------------------------------
# 👁 PROCESS EACH FILE
# -------------------------------------------------------------
async def process_file(uploaded_file, data, dfs, folder_name, request):

    fileName = uploaded_file.name
    uploaded_file.seek(0)  # ensure pointer is always fresh

    resume_link = save_resume_locally(uploaded_file, request)

    try:
        # PDF
        if fileName.lower().endswith(".pdf"):
            op = await extract_pdf_data(uploaded_file)

        # DOCX
        elif fileName.lower().endswith(".docx"):
            op = await extract_text_from_docx_file(uploaded_file)

        # XLSX
        elif fileName.lower().endswith(".xlsx"):
            df = await read_excel(uploaded_file)
            dfs.append(df)
            return

        else:
            print(f"Unsupported file type: {fileName}")
            return

        # Add resume link
        if op and isinstance(op, list) and len(op) > 0:
            op[0]["Resume_Link"] = resume_link

        # Add final cleaned data
        data.extend(findunique(data, op, fileName, folder_name))

    except Exception as e:
        print(f"Error processing {fileName}: {e}")


# -------------------------------------------------------------
# 📑 TEXT ANALYZER — Extracts email, phone, skills, etc.
# -------------------------------------------------------------
def extract_info(data):
    dic = {"Phone_Number": None, "Email_id": None, "Name_from_Email": None}

    technologies_pattern = r'\b(' + '|'.join(map(re.escape, technologies)) + r')\b'
    phone_pattern = r"(?:\+\d{1,3}\s?)?\d{10}"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    skills = set()

    if not isinstance(data, list):
        data = data.split('\n')

    # Save name lines
    dic["Name_Line1"] = data[0][:20] if len(data) else "NA"
    dic["Name_Line2"] = data[1][:20] if len(data) > 1 else "NA"

    for line in data:

        # Phone
        if not dic["Phone_Number"]:
            m = re.findall(phone_pattern, line)
            if m:
                dic["Phone_Number"] = m[0]

        # Email
        if not dic["Email_id"]:
            m = re.findall(email_pattern, line)
            if m:
                dic["Email_id"] = m[0]
                dic["Name_from_Email"] = re.sub(r'\d', '', m[0].split("@")[0])

        # Skills
        s = re.findall(technologies_pattern, line, re.IGNORECASE)
        for skill in s:
            skills.add(skill)

    dic["skills"] = list(skills)
    return dic


# -------------------------------------------------------------
# 🚀 MAIN VIEW — PROCESS ALL RESUMES
# -------------------------------------------------------------
async def process_salary(request):

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        folder_name = request.POST.get('folderName', 'default')

        if not uploaded_files:
            return HttpResponse("Please choose at least one file.")

        data = []
        dfs = []
        tasks = []

        for f in uploaded_files:
            tasks.append(process_file(f, data, dfs, folder_name, request))

        await asyncio.gather(*tasks)

        try:
            # If resume extracted
            if data:
                df = pd.DataFrame(data)

                # Make hyperlink clickable in Excel
                df["Resume_Link"] = df["Resume_Link"].apply(
                    lambda x: f'=HYPERLINK("{x}", "Open Resume")'
                )

                file_name = f'{folder_name}_employee_resumes.xlsx'
                df.to_excel(file_name, index=False)

            # If only Excel files uploaded
            elif dfs:
                merged = pd.concat(dfs, ignore_index=True)
                merged = merged.drop_duplicates(subset=['Email_id'])
                file_name = f'{folder_name}_merged.xlsx'
                merged.to_excel(file_name, index=False)

            else:
                return HttpResponse("No valid data found. Try again.")

            with open(file_name, 'rb') as fh:
                resp = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                resp["Content-Disposition"] = f'attachment; filename={file_name}'

                global duplicates_count
                print("Duplicates found:", duplicates_count)
                duplicates_count = 0

                return resp

        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return render(request, "temp2.html")



# -------------------------------------------------------------
# TECHNOLOGIES LIST (KEEP YOUR ORIGINAL FULL LIST)
# -------------------------------------------------------------
technologies = [
    # 🔥 keep your full list here (unchanged)
]

