from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class CodeInput(BaseModel):
    text: str

def clean_abap_code(code: str) -> str:
    cleaned_lines = []
    for line in code.splitlines():
        line_before_quote = line.split('"',1)[0].rstrip()
        cleaned_lines.append(line_before_quote)
    return "\n".join(cleaned_lines)

@app.post("/clean_abap/")
async def clean_abap(input_data: CodeInput):
    cleaned_code = clean_abap_code(input_data.code)
    return {"cleaned_code": cleaned_code}