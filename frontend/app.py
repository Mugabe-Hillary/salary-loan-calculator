import streamlit as st
import requests
import pandas as pd

# --- API Configuration ---
# Use the service name 'backend' when running with Docker Compose
# Otherwise, use 'localhost' or '127.0.0.1' for local testing
BACKEND_API_URL = "http://backend:8000" # For Docker Compose
# BACKEND_API_URL = "http://localhost:8000" # For local testing without Docker Compose

# --- Page Configuration ---
st.set_page_config(
    page_title="FinTech Calculator",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("💰 Advanced Salary & Loan Calculator")
st.markdown("---")

# Initialize session state for results to persist across reruns
if 'advance_result' not in st.session_state:
    st.session_state.advance_result = None
if 'loan_result' not in st.session_state:
    st.session_state.loan_result = None

# --- Salary Information Section ---
st.header("Personal & Salary Information")
with st.container(border=True):
    gross_salary = st.number_input(
        "Gross Monthly Salary ($)",
        min_value=0.01,
        value=3000.00,
        step=100.00,
        format="%.2f",
        help="Your total monthly earnings before deductions."
    )
    pay_frequency_options = ["Monthly", "Bi-Weekly", "Weekly"]
    pay_frequency = st.selectbox(
        "Pay Frequency",
        options=pay_frequency_options,
        index=0,
        help="How often you get paid."
    )
    st.markdown("---")


# --- Salary Advance Section ---
st.header("Salary Advance Request")
with st.form("advance_form", clear_on_submit=False):
    advance_amount = st.number_input(
        "Desired Advance Amount ($)",
        min_value=0.00,
        value=500.00,
        step=50.00,
        format="%.2f",
        help="The amount of salary advance you wish to request."
    )

    # Basic client-side validation for advance amount
    if advance_amount > gross_salary * 0.5: # Example policy: max 50% of gross salary
        st.warning(f"Advance amount typically limited to 50% of gross salary (${gross_salary * 0.5:.2f}).")
    elif advance_amount <= 0:
        st.error("Advance amount must be positive.")

    advance_submitted = st.form_submit_button("Calculate Advance Eligibility")

    if advance_submitted:
        # Prepare payload for FastAPI
        advance_payload = {
            "gross_monthly_salary": gross_salary,
            "pay_frequency": pay_frequency,
            "desired_advance_amount": advance_amount
        }
        st.info("Sending request to backend for advance calculation...")
        try:
            # Make API call to backend
            response = requests.post(f"{BACKEND_API_URL}/calculate_advance", json=advance_payload)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            st.session_state.advance_result = response.json()
            st.success("Advance calculation complete!")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend API. Please ensure the backend is running.")
            st.session_state.advance_result = None
        except requests.exceptions.RequestException as e:
            st.error(f"Error during advance calculation: {e}")
            st.session_state.advance_result = None
        st.rerun() # Rerun to display results immediately

st.markdown("---")


# --- Loan Calculation Section ---
st.header("Loan Calculation")
with st.form("loan_form", clear_on_submit=False):
    loan_amount = st.number_input(
        "Desired Loan Amount ($)",
        min_value=0.00,
        value=5000.00,
        step=100.00,
        format="%.2f",
        help="The total principal amount of the loan."
    )
    interest_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.01,
        value=5.00,
        max_value=100.00,
        step=0.10,
        format="%.2f",
        help="The annual interest rate for the loan."
    )
    loan_term_months = st.number_input(
        "Loan Term (Months)",
        min_value=1,
        value=12,
        max_value=60,
        step=1,
        help="The duration of the loan in months."
    )

    # Basic client-side validation for loan inputs
    if loan_amount <= 0:
        st.error("Loan amount must be positive.")
    if interest_rate <= 0:
        st.error("Interest rate must be positive.")
    if loan_term_months <= 0:
        st.error("Loan term must be positive.")

    loan_submitted = st.form_submit_button("Calculate Loan Repayment")

    if loan_submitted:
        # Prepare payload for FastAPI
        loan_payload = {
            "loan_amount": loan_amount,
            "annual_interest_rate": interest_rate,
            "loan_term_months": loan_term_months
        }
        st.info("Sending request to backend for loan calculation...")
        try:
            # Make API call to backend
            response = requests.post(f"{BACKEND_API_URL}/calculate_loan", json=loan_payload)
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            st.session_state.loan_result = response.json()
            st.success("Loan calculation complete!")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend API. Please ensure the backend is running.")
            st.session_state.loan_result = None
        except requests.exceptions.RequestException as e:
            st.error(f"Error during loan calculation: {e}")
            st.session_state.loan_result = None
        st.rerun() # Rerun to display results immediately

# --- Display Actual Results from Backend ---
st.markdown("---")
st.header("Calculation Results")

if st.session_state.advance_result:
    st.subheader("Salary Advance Result")
    result = st.session_state.advance_result
    if result["eligible"]:
        st.success(f"Advance Approved! {result['message']}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Approved Amount", f"${result['approved_amount']:.2f}")
        with col2:
            st.metric("Associated Fees", f"${result['fees']:.2f}")
        st.metric("Total Advance (Approved + Fees)", f"${result['approved_amount'] + result['fees']:.2f}")
    else:
        st.error(f"Advance Not Approved: {result.get('message', 'Reason unknown.')}")
    st.markdown("---")

if st.session_state.loan_result:
    st.subheader("Loan Calculation Result")
    result = st.session_state.loan_result
    st.info(result.get('message', 'Loan calculation complete.'))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Principal Amount", f"${result['principal']:.2f}")
    with col2:
        st.metric("Annual Interest Rate", f"{result['annual_interest_rate']:.2f}%")
    with col3:
        st.metric("Loan Term", f"{result['loan_term_months']} months")

    st.markdown("<br>", unsafe_allow_html=True) # Add some space

    col_repay, col_interest, col_monthly = st.columns(3)
    with col_repay:
        st.metric("Total Repayable", f"${result['total_repayable']:.2f}")
    with col_interest:
        st.metric("Total Interest Accrued", f"${result['total_interest_accrued']:.2f}")
    with col_monthly:
        st.metric("Estimated Monthly Payment", f"${result['monthly_payment']:.2f}")


    # Display Amortization Schedule if available
    if result.get("amortization_schedule"):
        st.subheader("Amortization Schedule")
        df_amortization = pd.DataFrame(result["amortization_schedule"])
        st.dataframe(df_amortization.style.format({
            "starting balance": "${:.2f}",
            "monthly_payment": "${:.2f}",
            "principal_payment": "${:.2f}",
            "interest_payment": "${:.2f}",
            "pending_balance": "${:.2f}"
        }), use_container_width=True)
    else:
        st.warning("Amortization schedule not available for these parameters.")
    st.markdown("---")


# Add a sidebar for general info or future features
with st.sidebar:
    st.header("About This App")
    st.info("This is an Advanced Salary & Loan Calculator. It's designed as a multi-container FinTech microservice application.")
    st.markdown("---")
    st.write("Developed by AMH \u00A9 2025")

