import streamlit as st
import pdfplumber
import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

st.title("💼 CreditLens AI - Advanced Version")

# Load trained model
model = pickle.load(open("credit_model.pkl", "rb"))

uploaded_file = st.file_uploader("Upload Company PDF", type=["pdf"])

def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def scrape_news(company_name):
    url = f"https://www.google.com/search?q={company_name}+news"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.title.string

def generate_cam(decision, loan, interest):
    file_path = "Generated_CAM_Report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Credit Appraisal Memo", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"Decision: {decision}", styles['Normal']))
    elements.append(Paragraph(f"Loan Amount: {loan}", styles['Normal']))
    elements.append(Paragraph(f"Interest Rate: {interest}", styles['Normal']))

    doc.build(elements)
    return file_path

if uploaded_file:
    text = extract_text(uploaded_file)
    st.subheader("Extracted Text Preview")
    st.write(text[:800])

    gst = st.number_input("GST Revenue", value=12)
    bank = st.number_input("Bank Inflow", value=7)
    litigation = st.checkbox("Litigation Found?")
    capacity = st.slider("Capacity %", 0, 100, 40)

    if st.button("Analyze"):
        input_data = pd.DataFrame([[gst, bank, int(litigation), capacity]],
                                  columns=["gst_revenue", "bank_inflow", "litigation_flag", "capacity_percent"])

        prediction = model.predict(input_data)[0]

        if prediction == 1:
            decision = "Approved"
            loan = "₹10 Crore"
            interest = "10%"
        else:
            decision = "Rejected"
            loan = "₹0"
            interest = "N/A"

        st.subheader("Final Decision")
        st.write(f"Decision: {decision}")
        st.write(f"Loan: {loan}")
        st.write(f"Interest: {interest}")

        news = scrape_news("ABC Manufacturing")
        st.subheader("News Analysis")
        st.write(news)

        cam_file = generate_cam(decision, loan, interest)

        with open(cam_file, "rb") as f:
            st.download_button("Download CAM Report", f, file_name="CAM_Report.pdf")