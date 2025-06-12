from pydantic import BaseModel, Field
from typing import Optional

# Pydantic model for the Salary Advance request
class AdvanceRequest(BaseModel):
    """
    Defines the structure for a salary advance request.
    """
    gross_monthly_salary: float = Field(..., gt=0, description="Gross monthly salary of the applicant.")
    pay_frequency: str = Field(..., description="Frequency of payment (e.g., Monthly, Bi-Weekly, Weekly).")
    desired_advance_amount: float = Field(..., gt=0, description="The amount of salary advance requested.")

# Pydantic model for the Salary Advance response
class AdvanceResponse(BaseModel):
    """
    Defines the structure for a salary advance eligibility response.
    """
    eligible: bool = Field(..., description="True if the advance is approved, False otherwise.")
    approved_amount: float = Field(..., ge=0, description="The approved advance amount.")
    fees: float = Field(..., ge=0, description="Any fees associated with the advance.")
    message: str = Field(..., description="A message explaining the eligibility status or outcome.")

# Pydantic model for the Loan Calculation request
class LoanRequest(BaseModel):
    """
    Defines the structure for a loan calculation request.
    """
    loan_amount: float = Field(..., gt=0, description="The principal amount of the loan.")
    annual_interest_rate: float = Field(..., gt=0, description="Annual interest rate in percentage.")
    loan_term_months: int = Field(..., gt=0, description="Loan term in months.")

# Pydantic model for the Loan Calculation response
class LoanResponse(BaseModel):
    """
    Defines the structure for a loan calculation response.
    Includes principal, interest, and monthly payment details.
    """
    principal: float = Field(..., description="The principal loan amount.")
    annual_interest_rate: float = Field(..., description="The annual interest rate applied.")
    loan_term_months: int = Field(..., description="The loan term in months.")
    total_repayable: float = Field(..., description="Total amount to be repaid over the loan term.")
    total_interest_accrued: float = Field(..., description="Total interest accrued over the loan term.")
    monthly_payment: float = Field(..., description="Estimated monthly payment.")
    amortization_schedule: Optional[list[dict]] = Field(None, description="Optional: Detailed amortization schedule.")
    message: str = Field(..., description="A message about the calculation status.")

 