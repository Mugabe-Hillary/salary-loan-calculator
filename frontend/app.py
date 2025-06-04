import streamlit as st
import requests
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

st.set_page_config(page_title="Salary Loan Calculator", layout="centered")
st.title("Salary Loan Calculator")

# Sidebar for defaults
with st.sidebar:
    st.header("Defaults")
    default_interest = st.slider("Default Annual Interest Rate (%)", 1.0, 30.0, 15.0)
    default_dti = st.slider("Max DTI Ratio", 0.1, 0.6, 0.4)

with st.form("loan_form"):
    st.subheader("Loan Details")

    gross_salary = st.number_input(
        "Gross Monthly Salary", min_value=0.0, value=1000000.0, step=1000.0
    )
    loan_amount = st.number_input(
        "Desired Loan Amount", min_value=0.0, value=5000000.0, step=1000.0
    )
    loan_term = st.number_input("Loan Term (months)", min_value=1, value=24, step=1)
    interest_rate = st.number_input(
        "Interest Rate (annual, %)", min_value=0.1, value=default_interest, step=0.1
    )
    deductions = st.number_input(
        "Monthly Deductions", min_value=0.0, value=0.0, step=100.0
    )

    submitted = st.form_submit_button("Calculate")

if submitted:
    payload = {
        "gross_salary": gross_salary,
        "loan_amount": loan_amount,
        "loan_term_months": loan_term,
        "annual_interest_rate": interest_rate,
        "deductions": deductions,
    }

    with st.spinner("Calculating..."):
        try:
            res = requests.post("http://backend:8000/calculate-loan", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.success("Loan Details Calculated")

                # Display metrics
                st.metric("Monthly Repayment", f"{data['monthly_payment']:.2f} UGX")
                st.metric("Total Repayment", f"{data['total_repayment']:.2f} UGX")
                st.metric("Total Interest", f"{data['total_interest']:.2f} UGX")
                st.metric("Max Eligible Loan", f"{data['max_eligible_loan']:.2f} UGX")

                # --- Chart Visualization ---
                labels = [
                    "Monthly Payment",
                    "Total Repayment",
                    "Total Interest",
                    "Max Eligible Loan",
                ]
                values = [
                    data["monthly_payment"],
                    data["total_repayment"],
                    data["total_interest"],
                    data["max_eligible_loan"],
                ]

                fig, ax = plt.subplots(figsize=(8, 4))
                bars = ax.bar(
                    labels, values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
                )
                ax.set_title("Loan Summary")
                ax.bar_label(bars, fmt="%.0f")
                ax.tick_params(axis="x", rotation=15)

                st.pyplot(fig)

                # --- PDF Export ---
                def create_pdf() -> bytes:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=16)
                    pdf.cell(0, 10, "Salary Loan Calculator Report", ln=True, align="C")

                    pdf.set_font("Arial", size=12)
                    pdf.ln(10)
                    pdf.cell(0, 10, "Input Parameters:", ln=True)
                    pdf.set_font("Arial", size=10)
                    pdf.cell(0, 8, f"Gross Salary: {gross_salary:,.2f} UGX", ln=True)
                    pdf.cell(
                        0, 8, f"Desired Loan Amount: {loan_amount:,.2f} UGX", ln=True
                    )
                    pdf.cell(0, 8, f"Loan Term (months): {loan_term}", ln=True)
                    pdf.cell(
                        0, 8, f"Interest Rate (annual %): {interest_rate:.2f}", ln=True
                    )
                    pdf.cell(
                        0, 8, f"Monthly Deductions: {deductions:,.2f} UGX", ln=True
                    )

                    pdf.ln(10)
                    pdf.set_font("Arial", size=12)
                    pdf.cell(0, 10, "Calculated Results:", ln=True)
                    pdf.set_font("Arial", size=10)
                    pdf.cell(
                        0,
                        8,
                        f"Monthly Payment: {data['monthly_payment']:,.2f} UGX",
                        ln=True,
                    )
                    pdf.cell(
                        0,
                        8,
                        f"Total Repayment: {data['total_repayment']:,.2f} UGX",
                        ln=True,
                    )
                    pdf.cell(
                        0,
                        8,
                        f"Total Interest: {data['total_interest']:,.2f} UGX",
                        ln=True,
                    )
                    pdf.cell(
                        0,
                        8,
                        f"Max Eligible Loan: {data['max_eligible_loan']:,.2f} UGX",
                        ln=True,
                    )

                    # Output PDF as bytes
                    pdf_data = pdf.output(dest="S")
                    if isinstance(pdf_data, str):
                        return pdf_data.encode("latin1")
                    elif isinstance(pdf_data, bytes):
                        return pdf_data
                    else:
                        raise TypeError(
                            f"Unexpected type for pdf output: {type(pdf_data)}"
                        )

                pdf_bytes: bytes = create_pdf()
                st.download_button(
                    label="Download Loan Report as PDF",
                    data=data(pdf_bytes),
                    file_name="salary_loan_report.pdf",
                    mime="application/pdf",
                )

            else:
                st.error("Error in response from backend.")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
