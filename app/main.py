from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class CodeInput(BaseModel):
    text: str

def clean_abap_code(code: str) -> str:
    cleaned_lines = []
    for line in code.splitlines():
        # skip lines that start with *
        if line.lstrip().startswith("*"):
            continue

        # remove inline comment starting with "
        line_before_quote = line.split('"', 1)[0].rstrip()

        # normalize multiple dots at the end to a single dot
        line_before_quote = re.sub(r"\.+\s*\.$", ".", line_before_quote.strip())

        # add line only if something remains
        if line_before_quote.strip():
            cleaned_lines.append(line_before_quote)

    return "\n".join(cleaned_lines)

@app.post("/clean_abap/")
async def clean_abap(input_data: CodeInput):
    cleaned_code = clean_abap_code(input_data.text)
    return {"cleaned_code": cleaned_code}
