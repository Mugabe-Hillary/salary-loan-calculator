from fastapi import FastAPI
from pydantic import BaseModel, Field
from math import pow
from .schemas import LoanOutput, LoanInput

app = FastAPI()


@app.post("/calculate-loan", response_model=LoanOutput)
def calculate_loan(data: LoanInput):
    monthly_rate = data.annual_interest_rate / 12 / 100
    n = data.loan_term_months
    A = data.loan_amount

    monthly_payment = (A * monthly_rate) / (1 - pow(1 + monthly_rate, -n))
    total_payment = monthly_payment * n
    total_interest = total_payment - A

    # Industry-standard Debt-To-Income ratio (e.g., 40%)
    max_loan_limit = 0.4 * (data.gross_salary - data.deductions)

    # Reverse amortization to estimate max loan eligibility
    eligible_loan = (max_loan_limit * (1 - pow(1 + monthly_rate, -n))) / monthly_rate

    return LoanOutput(
        monthly_payment=round(monthly_payment, 2),
        total_repayment=round(total_payment, 2),
        total_interest=round(total_interest, 2),
        max_eligible_loan=round(eligible_loan, 2),
    )
