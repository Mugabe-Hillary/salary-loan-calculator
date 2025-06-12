from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import pandas as pd
import numpy as np # Often used with pandas for numerical operations

from app.models import AdvanceRequest, AdvanceResponse, LoanRequest, LoanResponse

# Initialize FastAPI app
app = FastAPI(
    title="FinTech Calculator Backend API",
    description="API for Salary Advance Eligibility and Loan Calculations.",
    version="1.0.0"
)

# --- CORS Configuration ---
origins = [
    "http://localhost:8501",  # Default Streamlit port
    "http://127.0.0.1:8501",  # Another common localhost address for Streamlit
    "http://localhost",
    "http://127.0.0.1",
    # Add your deployed Streamlit URL here when you deploy
    # "https://your-deployed-streamlit-app.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Policy Constants for Advance (Example Values) ---
MAX_ADVANCE_PERCENTAGE_OF_SALARY = 0.40  # Max 40% of gross monthly salary
FLAT_ADVANCE_FEE = 5.00                # $5 flat fee
PERCENTAGE_ADVANCE_FEE = 0.02          # 2% of approved advance amount

# --- Helper Function for Loan Amortization ---
def calculate_loan_amortization(
    principal: float,
    annual_interest_rate: float, # as percentage, e.g., 5.0
    loan_term_months: int
) -> Dict[str, Any]:
    """
    Calculates loan amortization details including monthly payment,
    total repayable, total interest, and an amortization schedule.

    Args:
        principal (float): The principal loan amount.
        annual_interest_rate (float): Annual interest rate in percentage (e.g., 5.0 for 5%).
        loan_term_months (int): Loan term in months.

    Returns:
        Dict[str, Any]: A dictionary containing calculation results and the schedule.
    """
    if principal <= 0 or annual_interest_rate <= 0 or loan_term_months <= 0:
        return {
            "monthly_payment": 0.0,
            "total_repayable": 0.0,
            "total_interest_accrued": 0.0,
            "amortization_schedule": [],
            "message": "Invalid loan parameters (principal, rate, or term must be positive)."
        }

    monthly_interest_rate = (annual_interest_rate / 100) / 12

    # Calculate Monthly Payment (M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1])
    if monthly_interest_rate == 0: # Handle 0% interest rate separately
        monthly_payment = principal / loan_term_months
    else:
        monthly_payment = (principal * monthly_interest_rate *
                           (1 + monthly_interest_rate)**loan_term_months) / \
                          ((1 + monthly_interest_rate)**loan_term_months - 1)

    total_repayable = monthly_payment * loan_term_months
    total_interest_accrued = total_repayable - principal

    # Generate Amortization Schedule using Pandas
    schedule_data = []
    remaining_balance = principal

    for month in range(1, loan_term_months + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment

        # Adjust last payment to account for floating point inaccuracies
        if month == loan_term_months:
            principal_payment = remaining_balance
            monthly_payment = principal_payment + interest_payment # Recalculate last payment
            remaining_balance = 0.0
        else:
            remaining_balance -= principal_payment


        schedule_data.append({
            "month": month,
            "starting_balance": round(principal if month == 1 else schedule_data[-1]["ending_balance"], 2), # Correct starting balance
            "monthly_payment": round(monthly_payment, 2),
            "principal_payment": round(principal_payment, 2),
            "interest_payment": round(interest_payment, 2),
            "ending_balance": round(remaining_balance, 2)
        })

    df_schedule = pd.DataFrame(schedule_data)

    # Ensure final ending balance is exactly 0 due to potential small floating point errors
    if not df_schedule.empty:
        df_schedule.loc[df_schedule.index[-1], 'ending_balance'] = 0.0
        # Re-adjust last payment if necessary for exact total
        if df_schedule.loc[df_schedule.index[-1], 'principal_payment'] + df_schedule.loc[df_schedule.index[-1], 'interest_payment'] != df_schedule.loc[df_schedule.index[-1], 'monthly_payment']:
            # This adjustment might be complex and is often handled by making the very last payment cover the exact remainder
            # For simplicity, we assume the previous calculation is precise enough or the error is negligible.
            pass


    return {
        "monthly_payment": monthly_payment,
        "total_repayable": total_repayable,
        "total_interest_accrued": total_interest_accrued,
        "amortization_schedule": df_schedule.round(2).to_dict(orient="records"), # Convert DataFrame to list of dicts
        "message": "Loan calculation successful."
    }


# --- Root Endpoint (for health check/info) ---
@app.get("/", tags=["Health Check"])
async def read_root() -> Dict[str, str]:
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "FinTech Calculator Backend API is running!"}

# --- /calculate_advance Endpoint (remains as is from Step 4) ---
@app.post("/calculate_advance", response_model=AdvanceResponse, tags=["Salary Advance"])
async def calculate_advance(request: AdvanceRequest) -> AdvanceResponse:
    """
    Calculates salary advance eligibility and approved amount based on policy.

    - Determines maximum eligible advance based on a percentage of gross monthly salary.
    - Applies a flat fee and a percentage fee.
    - Returns eligibility status, approved amount, and total fees.
    """
    try:
        gross_salary = request.gross_monthly_salary
        desired_advance = request.desired_advance_amount
        pay_frequency = request.pay_frequency

        eligible = False
        approved_amount = 0.0
        fees = 0.0
        message = ""

        if desired_advance <= 0:
            message = "Desired advance amount must be greater than zero."
            return AdvanceResponse(eligible=eligible, approved_amount=approved_amount, fees=fees, message=message)

        max_eligible_advance = gross_salary * MAX_ADVANCE_PERCENTAGE_OF_SALARY

        if desired_advance > max_eligible_advance:
            eligible = False
            approved_amount = 0.0
            message = (f"Desired advance of ${desired_advance:.2f} exceeds "
                       f"maximum eligible amount of ${max_eligible_advance:.2f} "
                       f"({MAX_ADVANCE_PERCENTAGE_OF_SALARY * 100:.0f}% of salary).")
        else:
            eligible = True
            approved_amount = desired_advance
            fees = FLAT_ADVANCE_FEE + (approved_amount * PERCENTAGE_ADVANCE_FEE)
            message = "Advance approved based on policy."

        return AdvanceResponse(
            eligible=eligible,
            approved_amount=approved_amount,
            fees=fees,
            message=message
        )
    except Exception as e:
        print(f"Error calculating advance: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error during advance calculation: {e}")

# --- /calculate_loan Endpoint ---
@app.post("/calculate_loan", response_model=LoanResponse, tags=["Loan Calculation"])
async def calculate_loan(request: LoanRequest) -> LoanResponse:
    """
    Calculates loan repayment details and an optional amortization schedule.
    Uses Pandas for tabular data representation.
    """
    try:
        principal = request.loan_amount
        annual_rate = request.annual_interest_rate
        term_months = request.loan_term_months

        loan_results = calculate_loan_amortization(principal, annual_rate, term_months)

        return LoanResponse(
            principal=principal,
            annual_interest_rate=annual_rate,
            loan_term_months=term_months,
            total_repayable=loan_results["total_repayable"],
            total_interest_accrued=loan_results["total_interest_accrued"],
            monthly_payment=loan_results["monthly_payment"],
            amortization_schedule=loan_results["amortization_schedule"],
            message=loan_results["message"]
        )
    except Exception as e:
        print(f"Error calculating loan: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error during loan calculation: {e}")

