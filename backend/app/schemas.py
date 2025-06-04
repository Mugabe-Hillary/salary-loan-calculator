from pydantic import BaseModel, Field


# Input model
class LoanInput(BaseModel):
    gross_salary: float = Field(gt=0, description="Gross monthly salary")
    loan_amount: float = Field(gt=0, description="Desired loan amount")
    loan_term_months: int = Field(gt=0, description="Loan term in months")
    annual_interest_rate: float = Field(
        gt=0, description="Annual interest rate (percentage)"
    )
    deductions: float = Field(
        ge=0, default=0.0, description="Optional monthly deductions"
    )


# Output model
class LoanOutput(BaseModel):
    monthly_payment: float
    total_repayment: float
    total_interest: float
    max_eligible_loan: float
