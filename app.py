import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input_text)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


# Prompt Template
input_prompt_template = """
As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing Software Engineering, Data Science, 
Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer, DevOps Engineer, Machine Learning Engineer, 
Cybersecurity Analyst, Cloud Solutions Architect, Database Administrator, Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, 
UI/UX Designer, IT Project Manager, and additional specialized areas, your objective is to meticulously assess resumes against provided job descriptions.
In a fiercely competitive job market, your expertise is crucial in offering top-notch guidance for resume enhancement. 
Assign precise matching percentages based on the JD (Job Description) and meticulously identify any missing keywords with utmost accuracy.


resume: {resume_text}
description: {jd}


I want the response in the following structure:
The first line indicates the percentage match with the job description (JD).
The second line presents a list of missing keywords.
The third section provides a profile summary.
Mention the title for all the three sections.


While generating the response put some space to separate all the three sections.
"""

# Streamlit App
st.title("Resume ATS Tracker")
st.text("Improve Your Resume's ATS Compatibility")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt_template.format(resume_text=resume_text, jd=jd)
        response = get_gemini_response(input_prompt)
        st.subheader("Evaluation Result")
        st.text(response)