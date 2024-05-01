from pydantic import BaseModel


class AudioGenerationRequest(BaseModel):
    text: str
