from pydantic import BaseModel, Field

class EmploymentCheck(BaseModel):
    has_matched: bool = Field(description="True if the ad offers one of the target employment types")