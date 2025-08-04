from pydantic import BaseModel,Field
from typing import Any, Dict, List, Optional,Literal
from datetime import date

class EmployeeCreate(BaseModel):
  first_name: str=Field(...,description="First name of the Employee", example="John")
  last_name: str=Field(...,description="Last name of the Employee", example="Doe")
  location: Literal['Noida', 'Gurgaon', 'Bangalore', 'Hyderabad']=Field(...,description="Location of the Employee", example="Noida")
  role: Literal['Manager', 'Associate', 'Supervisor', 'Assistant Manager']=Field(...,description="Role of the Employee")
  department: Literal['HR', 'IT', 'Finance', 'Marketing']=Field(...,description="Department of the Employee", example="IT")
  joined_date: date=Field(...,description="Joining date of the Employee", example="2021-01-01")
  dob: date=Field(...,description="Date of birth of the Employee", example="1990-01-01")
  supervisor_name: Optional[str] = Field(None,description="Supervisor name of the Employee", example="Jane Doe")
