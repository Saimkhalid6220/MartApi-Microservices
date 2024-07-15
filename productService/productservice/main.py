from fastapi import FastAPI

app = FastAPI()

@app.get('/product')
def read_root():
    return {"hello":"world"}