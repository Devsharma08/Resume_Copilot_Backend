from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field

class ResumeCreate(BaseModel):
    description:str | None= Field(
        max_length=1024 ,
        default=None ,
        description="optional description of the resume"
    )
    title:str = Field(
        ...,
        max_length = 100 ,
        min_length = 1 ,
        description = "Title of the resume profile"
    )

class ResumeUpdate(BaseModel):
    description:str | None = Field(
        max_length=1024 ,
        default=None ,
        description="optional description of the resume"
    )
    title:str | None = Field(
        default=None ,
        max_length = 100 ,
        min_length = 1 ,
        description = "Title of the resume profile"
    )


class ResumeResponse(BaseModel):
    id:int
    title:str
    description:str | None
    created_at:datetime
    updated_at:datetime
    user_id:int
    model_config = ConfigDict(from_attributes=True)
