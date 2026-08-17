from pydantic import BaseModel, Field
from typing import List, Optional

class StudentProfile(BaseModel):
    cgpa: float = Field(..., ge=0.0, le=10.0)
    year_of_study: int = Field(..., ge=1, le=4)
    branch: str
    projects_built: int = Field(..., ge=0)
    internship_experience: int = Field(..., ge=0)
    risk_appetite: int = Field(..., ge=1, le=10)
    communication_preference: int = Field(..., ge=1, le=10)
    timeline_urgency: int = Field(..., ge=1, le=10)
    domain_interests: List[str] = Field(default_factory=list)
    target_company_type: str 
    open_confusion_text: Optional[str] = None