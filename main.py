# create a fastapi app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

import g4f

g4f.debug.logging = True  # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking


app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_methods=['*'],
  allow_headers=['*'],
)

class PromptIn(BaseModel):
  prompt: str

class PromptOut(BaseModel):
  prompt: str
  output: Optional[str] = None
  err: Optional[str] = None

@app.post('/prompt', response_model=PromptOut)
def call_llm(inp: PromptIn):
  retries = 5
  err = None
  for _ in range(retries):
    try:
      response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        # model=g4f.models.llama2_70b,
        # provider=g4f.Provider.DeepInfra,
        messages=[{"role": "user", "content": inp.prompt}],
        stream=False,
      )
      return PromptOut(prompt=inp.prompt, output=response)
    except Exception as e:
      print(f"Error occurred: {e}")
      err = str(e)
  return PromptOut(prompt=inp.prompt, err=err)  # Return None if all retries fail


if __name__ == '__main__':
  import uvicorn
  uvicorn.run("main:app", host='localhost', port=8000, reload=True)