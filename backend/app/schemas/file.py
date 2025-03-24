from pydantic import BaseModel

class FileResponse(BaseModel):
    filename: str
    prediction: str
    details: dict

    class Config:
        orm_mode = True
