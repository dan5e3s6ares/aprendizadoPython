from pydantic import BaseModel


class BasicLearn(BaseModel):
    text: str
    tag: str


class ConsultReturn(BasicLearn):
    id: str
    score: str
    content: str
    tag: str
